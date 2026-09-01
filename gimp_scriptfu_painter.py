#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GIMP Python-Fu & Script-Fu landscape painting generator
Can be executed directly via GIMP batch CLI or embedded python-fu console.
"""

def generate_script_fu_template():
    return """
; Script-Fu template for generating layered banner canvas in GIMP
(define (script-fu-auto-banner width height bg-color text-title)
  (let* ((image (car (gimp-image-new width height RGB)))
         (layer (car (gimp-layer-new image width height RGB-IMAGE "Background" 100 NORMAL-MODE))))
    (gimp-image-insert-layer image layer 0 0)
    (gimp-context-set-foreground bg-color)
    (gimp-drawable-fill layer FOREGROUND-FILL)
    (gimp-display-new image)
  )
)
"""

if __name__ == "__main__":
    print("Script-Fu Batch Template:")
    print(generate_script_fu_template())
