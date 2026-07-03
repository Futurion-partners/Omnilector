import numpy as np
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, List, Optional
from io import BytesIO
from PIL import Image, ImageOps, ImageFilter
try:
    import cv2
    OPENCV_AVAILABLE = True
    # Intentar inicializar el detector WeChat QR
    try:
        _test_detector = cv2.wechat_qrcode_WeChatQRCode()
        WECHAT_QR_AVAILABLE = True
    except Exception:
        WECHAT_QR_AVAILABLE = False
except ImportError:
    OPENCV_AVAILABLE = False
    WECHAT_QR_AVAILABLE = False
from pyzbar.pyzbar import decode as pyz_decode
try:
    import zxingcpp
    ZXING_AVAILABLE = True
except ImportError:
    ZXING_AVAILABLE = False

from futurion_barcode.models.responses.barcode import BarcodeResponse

# Instancias reutilizables
executor = ThreadPoolExecutor(max_workers=max(1, min(2, (os.cpu_count() or 2))))

class CodeTypeHeuristic:
    pass  # Heurísticas eliminadas: todo pasa por PyZbar

class OptimizedDetector:
    """Detector optimizado con estrategias paralelas"""
    
    def __init__(self):
        self.timeout_per_method = 2.0  # Timeout aumentado para mejor detección
        # Mantener referencia de la imagen original para confirmaciones cruzadas
        self._current_original: Optional[Image.Image] = None
        # Inicializar detector WeChat QR si está disponible
        self.wechat_detector = None
        if WECHAT_QR_AVAILABLE:
            try:
                self.wechat_detector = cv2.wechat_qrcode_WeChatQRCode()
            except Exception:
                pass
    
    async def detect_parallel(self, image: Image.Image, heuristics: dict) -> Tuple[List[str], List, List[str]]:
        """Ejecuta detección dando prioridad a WeChat QR, luego PyZbar y finalmente ZXing"""
        self._current_original = image
        
        # 1) WeChat QR primero (mejor para QR codes)
        if self.wechat_detector is not None:
            barcodes, locations = await self._run_with_timeout(self._detect_wechat_qr, image)
            if barcodes:
                self._current_original = None
                return barcodes, locations, ["wechat-qr"] * len(barcodes)
        
        # 2) PyZbar segundo
        barcodes, locations = await self._run_with_timeout(self._detect_pyzbar, image)
        if barcodes:
            self._current_original = None
            return barcodes, locations, ["pyzbar"] * len(barcodes)

        # 3) ZXing general como respaldo si está disponible
        if ZXING_AVAILABLE:
            barcodes, locations = await self._run_with_timeout(self._detect_zxing_general, image)
            if barcodes:
                pass

        self._current_original = None
        return barcodes, locations, (["zxing"] * len(barcodes) if barcodes else [])

    def _build_detection_pipeline(self, *args, **kwargs) -> List[Tuple]:
        # Compatibilidad: ya no se usa; mantenido por interfaz
        return [(self._detect_pyzbar, (), 'pyzbar')]

    # merge_results ya no es necesario en modo PyZbar-only
    
    async def _run_with_timeout(self, func, *args):
        """Ejecuta una función con timeout"""
        try:
            loop = asyncio.get_event_loop()
            return await asyncio.wait_for(
                loop.run_in_executor(executor, func, *args),
                timeout=self.timeout_per_method
            )
        except asyncio.TimeoutError:
            return [], []
        except Exception:
            return [], []
    async def _fallback_detection(self, *args, **kwargs) -> Tuple[List[str], List]:
        # Sin fallback en modo PyZbar-only
        return [], []
    
    def _generate_more_variants(self, *args, **kwargs) -> List[Tuple]:
        # Variantes deshabilitadas (sin OpenCV)
        return []
    
    def _detect_qr_fast(self, *args, **kwargs) -> Tuple[List[str], List]:
        # Deshabilitado (sin OpenCV)
        return [], []
    
    def _detect_1d_fast(self, *args, **kwargs) -> Tuple[List[str], List]:
        # Deshabilitado (sin OpenCV)
        return [], []
    
    def _detect_wechat_qr(self, image: Image.Image) -> Tuple[List[str], List]:
        """Detección con OpenCV WeChat QR (sin preprocesado)"""
        if self.wechat_detector is None:
            return [], []
        
        try:
            # Convertir PIL Image a formato OpenCV
            if image.mode != 'RGB':
                img = image.convert('RGB')
            else:
                img = image
            
            img_array = np.array(img)
            # OpenCV usa BGR, PIL usa RGB
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        except Exception:
            return [], []
        
        barcodes: List[str] = []
        locations: List = []
        
        try:
            # Detección directa sin preprocesado
            results, points = self.wechat_detector.detectAndDecode(img_bgr)
            
            if results and any(results):
                for i, text in enumerate(results):
                    if text:  # Solo agregar si el texto no está vacío
                        barcodes.append(text)
                        # Extraer coordenadas si están disponibles
                        if points is not None and len(points) > i:
                            try:
                                pts = points[i].reshape(-1, 2).astype(int).tolist()
                                locations.append(pts)
                            except Exception:
                                locations.append([])
                        else:
                            locations.append([])
        except Exception:
            pass
        
        return barcodes, locations
    
    def _detect_opencv_barcode(self, *args, **kwargs) -> Tuple[List[str], List]:
        # Deshabilitado (método legacy)
        return [], []
    
    def _detect_pyzbar(self, image: Image.Image) -> Tuple[List[str], List]:
        """Detección mejorada con OpenCV + PyZbar para códigos 1D difíciles"""
        if not OPENCV_AVAILABLE:
            # Fallback simple si OpenCV no está disponible
            return self._detect_pyzbar_simple(image)
        
        try:
            # Convertir a OpenCV
            img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        except Exception:
            return self._detect_pyzbar_simple(image)
        
        barcodes: List[str] = []
        locations: List = []
        seen_codes = set()
        
        def try_decode(img_variant, scale=1.0, offset_x=0, offset_y=0):
            """Intenta decodificar y agrega a resultados"""
            try:
                decoded = pyz_decode(img_variant)
            except Exception:
                decoded = []
            
            for d in decoded:
                try:
                    text = d.data.decode('utf-8', errors='ignore')
                    if text and text not in seen_codes:
                        seen_codes.add(text)
                        barcodes.append(text)
                        
                        # Ajustar coordenadas
                        rect = d.rect
                        pts = [
                            [int(rect.left / scale + offset_x), int(rect.top / scale + offset_y)],
                            [int((rect.left + rect.width) / scale + offset_x), int(rect.top / scale + offset_y)],
                            [int((rect.left + rect.width) / scale + offset_x), int((rect.top + rect.height) / scale + offset_y)],
                            [int(rect.left / scale + offset_x), int((rect.top + rect.height) / scale + offset_y)]
                        ]
                        locations.append(pts)
                except Exception:
                    continue
            return len(decoded) > 0
        
        # 1. Original
        if try_decode(gray):
            return barcodes, locations
        
        # 2. Morfología de cierre y apertura PRIORIZADA (funciona para la mayoría)
        try:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            closed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
            opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
            if try_decode(opened):
                return barcodes, locations
        except Exception:
            pass
        
        # 3. CLAHE + Morfología (combinación potente)
        try:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            # Aplicar morfología inmediatamente después de CLAHE
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            closed = cv2.morphologyEx(enhanced, cv2.MORPH_CLOSE, kernel)
            opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
            if try_decode(opened):
                return barcodes, locations
        except Exception:
            enhanced = gray
        
        # 4. Binarización Otsu
        try:
            _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            if try_decode(otsu):
                return barcodes, locations
        except Exception:
            otsu = gray
        
        # 5. Adaptive threshold (MUY importante para 1D)
        try:
            adaptive = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
            if try_decode(adaptive):
                return barcodes, locations
        except Exception:
            pass
        
        # 6. Morfología para limpiar códigos de barras binarizados
        try:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            morph_closed = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kernel)
            morph_opened = cv2.morphologyEx(morph_closed, cv2.MORPH_OPEN, kernel)
            if try_decode(morph_opened):
                return barcodes, locations
        except Exception:
            pass
        
        # 7. Upscaling solo si es necesario (códigos pequeños)
        try:
            h, w = gray.shape
            # Solo un scale factor óptimo
            resized = cv2.resize(enhanced, (int(w * 2.0), int(h * 2.0)), 
                                interpolation=cv2.INTER_CUBIC)
            if try_decode(resized, scale=2.0):
                return barcodes, locations
        except Exception:
            pass
        
        # 8. Inversión (códigos claros sobre fondo oscuro)
        try:
            inverted = 255 - enhanced
            if try_decode(inverted):
                return barcodes, locations
        except Exception:
            pass
        
        return barcodes, locations
    
    def _detect_pyzbar_simple(self, image: Image.Image) -> Tuple[List[str], List]:
        """Fallback simple sin OpenCV"""
        barcodes: List[str] = []
        locations: List = []
        
        try:
            decoded = pyz_decode(image)
        except Exception:
            decoded = []
        
        for d in decoded:
            try:
                text = d.data.decode('utf-8', errors='ignore')
                if not text:
                    continue
                rect = d.rect
                pts = [
                    [rect.left, rect.top],
                    [rect.left + rect.width, rect.top],
                    [rect.left + rect.width, rect.top + rect.height],
                    [rect.left, rect.top + rect.height]
                ]
                barcodes.append(text)
                locations.append(pts)
            except Exception:
                continue
        
        return barcodes, locations
    
    def _detect_zxing_general(self, image: Image.Image) -> Tuple[List[str], List]:
        """Detección general con ZXing (secundaria a PyZbar)"""
        if not ZXING_AVAILABLE:
            return [], []

        try:
            # Asegurar formato RGB
            if image.mode not in ("RGB", "L"):
                img = image.convert("RGB")
            else:
                img = image
            arr = np.array(img)
        except Exception:
            return [], []

        barcodes: List[str] = []
        locations: List = []
        try:
            # Intentar con opciones si existen
            results = None
            try:
                if hasattr(zxingcpp, 'ReaderOptions'):
                    opts = zxingcpp.ReaderOptions()
                    # Activar búsquedas más exhaustivas
                    if hasattr(opts, 'try_harder'):
                        setattr(opts, 'try_harder', True)
                    if hasattr(opts, 'try_rotate'):
                        setattr(opts, 'try_rotate', True)
                    results = zxingcpp.read_barcodes(arr, opts)
            except Exception:
                results = None
            if results is None:
                results = zxingcpp.read_barcodes(arr)
            for result in results or []:
                text = getattr(result, 'text', None)
                if text:
                    barcodes.append(text)
                    # Posiciones opcionales si están disponibles
                    pos = getattr(result, 'position', None)
                    if pos:
                        try:
                            locations.append([
                                [int(pos.top_left.x), int(pos.top_left.y)],
                                [int(pos.top_right.x), int(pos.top_right.y)],
                                [int(pos.bottom_right.x), int(pos.bottom_right.y)],
                                [int(pos.bottom_left.x), int(pos.bottom_left.y)],
                            ])
                        except Exception:
                            locations.append([])
                    else:
                        locations.append([])
        except Exception:
            pass

        return barcodes, locations

# Instancia global del detector optimizado
optimized_detector = OptimizedDetector()


async def process_image(contents: bytes) -> BarcodeResponse:
    """Procesamiento principal optimizado con mejor fallback"""
    # Decodificar imagen
    try:
        pil_image = Image.open(BytesIO(contents))
        pil_image.load()
        # Corregir orientación según EXIF (si aplica)
        try:
            pil_image = ImageOps.exif_transpose(pil_image)
        except Exception:
            pass
    except Exception:
        raise ValueError("Invalid image data")
    
    # Detección
    all_barcodes, all_locations, sources = await optimized_detector.detect_parallel(pil_image, heuristics=None)
    
    return BarcodeResponse(
        barcodes=all_barcodes,
        locations=all_locations,
        sources=sources
    )