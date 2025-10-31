# Coding Guidelines - Proyecto PHP

## Objetivo  
Este documento establece las reglas y buenas prácticas que se deben seguir al desarrollar en el proyecto, con el fin de garantizar un código limpio, consistente y mantenible.  

---

## 1. Separación de Estilos (CSS)

**Regla:**  
No se deben incluir estilos directamente en etiquetas HTML ni dentro de archivos PHP utilizando el atributo `style` o bloques `<style>`.  

**Correcto:**  
```html
<link rel="stylesheet" href="styles/main.css">
```

**Incorrecto:**  
```html
<select style="color:#404040; height:32px; ...">
```

**Justificación:**  
- Mejora la legibilidad y mantiene el código ordenado.  
- Facilita la reutilización de estilos en diferentes vistas.  
- Permite centralizar los cambios visuales en un único archivo CSS.  
- Favorece el versionamiento (Git) y la colaboración en equipo.  

---

## 2. Separación de Scripts (JavaScript)

**Regla:**  
No se deben escribir bloques de JavaScript directamente en archivos PHP ni en HTML usando `<script>` en línea. Toda lógica de JS debe estar en un archivo `.js` independiente.  

**Correcto:**  
```html
<script src="scripts/app.js"></script>
```

**Incorrecto:**  
```html
<script>
  document.getElementById("btn").onclick = function() { ... }
</script>
```

**Justificación:**  
- Claridad en la separación de responsabilidades (PHP = servidor, CSS = estilos, JS = comportamiento).  
- Facilita la depuración y mantenimiento del código.  
- Promueve la reutilización de funciones y módulos.  
- Reduce riesgos de inyección de código.  

---

## 3. Principio de Responsabilidad Única

Cada tipo de archivo debe cumplir una sola función:  

- **PHP:** lógica de servidor y renderizado de vistas.  
- **CSS:** presentación visual.  
- **JS:** comportamiento dinámico.  

**Beneficios:**  
- Mayor escalabilidad del proyecto.  
- Facilita la incorporación de nuevos desarrolladores.  
- Cumplimiento de estándares de calidad y buenas prácticas.  

---

## 4. Beneficios Generales de Estas Reglas

- Código más profesional y organizado.  
- Reducción de errores y conflictos entre desarrolladores.  
- Mayor facilidad para aplicar pruebas, auditorías y revisiones de código.  
- Preparación para escalar el proyecto a futuro con menos esfuerzo técnico.  

---

📌 **Nota:** Todo nuevo desarrollo o modificación debe respetar estas guías. Los Pull Requests que no cumplan estas reglas podrán ser rechazados hasta que se ajusten a los lineamientos establecidos.  
