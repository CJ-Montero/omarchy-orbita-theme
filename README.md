# Órbita

Tema espacial para Omarchy: espacio profundo azul oscuro, paneles azul más vivo,
acentos cian, bordes orbitales en degradado y un planeta con anillos como fondo.
Esta variante aumenta la saturación y luminosidad de la paleta original.

| Color | Hex | Uso |
|---|---|---|
| Bony / Ebony | `#0e1420` | Fondo y barra |
| Cloud burst, más vivo | `#243e63` | Paneles, menús y notificaciones |
| William, más vivo | `#3f7895` | Selecciones y bordes inactivos |
| Bermuda gray, más vivo | `#68b3d8` | Acentos y texto secundario |
| Tower gray, más luminoso | `#c0dbe0` | Texto principal y luces |

La paleta ANSI y la sintaxis también usan estos cinco colores. Omarchy genera
las configuraciones de terminales, editores y aplicaciones desde `colors.toml`.
Los archivos `shell.*.toml` ajustan los colores de las superficies de la shell.

## Transición de workspaces

`workspace_animation.lua` añade un deslizamiento horizontal con fundido,
aceleración suave y frenado gradual: 450 ms y un recorrido del 28% de la pantalla.
La configuración personal `~/.config/hypr/looknfeel.lua` carga este módulo después
de los ajustes generales. Al elegir un tema sin este módulo se recupera la
transición anterior (`slidefade 15%`, 500 ms, curva `softTiling`).

## Instalación

```bash
mkdir -p ~/.config/omarchy/themes/orbita
cp -a /home/cjmontero/Work/omarchy-orbita/. ~/.config/omarchy/themes/orbita/
omarchy theme set orbita
```

## Fondo

`backgrounds/orbita.png`: ilustración espacial panorámica 16:9 generada con la
herramienta integrada imagegen. El prompt completo está en `wallpaper-prompt.txt`.

Incluye también los 22 fondos del tema Artemis, conservando sus nombres originales.
Están disponibles en el selector de fondos de Órbita.

El tema activo antes de instalar Órbita era Artemis. Para volver:

```bash
omarchy theme set artemis
```
