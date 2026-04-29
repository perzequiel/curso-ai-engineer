# Guia de Entrega de Clases

Paso a paso detallado para entregar cada clase del curso. Segui estos pasos en orden para evitar errores.

---

## Paso 1: Clonar el repositorio (solo la primera vez)

Si es la **primera vez** que trabajas con el repositorio, clonalo:

```bash
git clone git@github.com:perzequiel/curso-ai-engineer.git
```

Ingresa a la carpeta del proyecto:

```bash
cd curso-ai-engineer
```

> Si ya tenes el repositorio clonado, pasa directamente al **Paso 2**.

---

## Paso 2: Actualizar el repositorio

**Siempre** antes de empezar una clase nueva, actualizá tu repositorio local para traer las ramas nuevas que se hayan creado:

```bash
git fetch --all
```

Verifica que la rama de la clase que vas a entregar existe:

```bash
git branch -r
```

Deberias ver algo como `origin/feature/clase-1_base`, `origin/feature/clase-2_base`, etc.

---

## Paso 3: Moverse a la rama de la clase

Posicionate en la rama de la clase que vas a trabajar. Por ejemplo, para la **clase 1**:

```bash
git checkout feature/clase-1_base
```

> Reemplaza el numero `1` por el numero de la clase que corresponda (clase-2_base, clase-3_base, etc.).

Asegurate de que tu rama local este actualizada con la remota:

```bash
git pull origin feature/clase-1_base
```

---

## Paso 4: Crear tu rama personal de trabajo

A partir de la rama de la clase, crea tu propia rama agregando tu nombre y apellido al final. El formato es:

```
feature/clase-[numero]_[nombre]-[apellido]
```

Por ejemplo, si te llamas **Juan Perez** y es la **clase 1**:

```bash
git checkout -b feature/clase-1_juan-perez
```

**Importante:**
- Usa todo en minusculas
- Separa nombre y apellido con guion medio (`-`)
- El separador entre el numero de clase y tu nombre es guion bajo (`_`)
- No uses espacios, tildes ni caracteres especiales

Verifica que estas parado en tu rama:

```bash
git branch
```

Deberia aparecer con un asterisco (`*`) tu rama, por ejemplo:

```
* feature/clase-1_juan-perez
```

---

## Paso 5: Completar la consigna

La consigna consiste en **hacer pasar los tests unitarios** de la clase correspondiente, aplicando lo visto durante la clase.

Los tests de cada clase se encuentran en:

```
tests/clase_[numero]/
```

Por ejemplo, para la clase 1 los tests estan en `tests/clase_1/`.

Para verificar que los tests pasan, ejecuta:

```bash
# Correr solo los tests de tu clase (ejemplo clase 1)
pytest tests/clase_1/ -v
```

Cuando **todos los tests pasen**, vas a ver algo asi:

```
========================= X passed in 0.XXs =========================
```

> **No avances al siguiente paso hasta que todos los tests pasen.** Si alguno falla, revisá tu codigo y volve a correr los tests.

---

## Paso 6: Hacer commit de tus cambios

Una vez que todos los tests pasan, agrega tus archivos modificados al staging area:

```bash
git add .
```

Verifica que los archivos correctos estan agregados:

```bash
git status
```

Deberias ver tus archivos modificados en verde bajo "Changes to be committed".

Crea el commit con un mensaje descriptivo:

```bash
git commit -m "clase-[numero]: resuelvo tests - [Nombre] [Apellido]"
```

Ejemplo:

```bash
git commit -m "clase-1: resuelvo tests - Juan Perez"
```

---

## Paso 7: Hacer push de tu rama

Subi tu rama al repositorio remoto:

```bash
git push origin feature/clase-1_juan-perez
```

> Reemplaza `feature/clase-1_juan-perez` con el nombre exacto de tu rama.

Si es la primera vez que pusheas esta rama, git la creara automaticamente en el remoto.

---

## Paso 8: Crear el Pull Request en GitHub

1. Ingresa al repositorio en GitHub: [https://github.com/perzequiel/curso-ai-engineer](https://github.com/perzequiel/curso-ai-engineer)
2. Vas a ver un banner amarillo que dice **"Compare & pull request"** para tu rama recien pusheada. Hace click ahi.
   - Si no aparece el banner, anda a la pestaña **"Pull requests"** > **"New pull request"**
3. Configura el Pull Request asi:
   - **base** (rama destino): `feature/clase-[numero]` (ejemplo: `feature/clase-1`)
   - **compare** (tu rama): `feature/clase-[numero]_[nombre]-[apellido]` (ejemplo: `feature/clase-1_juan-perez`)
4. En el titulo del PR pone: `Clase [numero] - [Nombre] [Apellido]`
   - Ejemplo: `Clase 1 - Juan Perez`
5. En la descripcion podes agregar comentarios sobre tu solucion si lo deseas
6. Hace click en **"Create pull request"**

**Verificacion importante:** Asegurate de que el PR apunte a `feature/clase-[numero]` y **NO** a `main`.

---

## Paso 9: Avisar en el grupo de WhatsApp

Una vez creado el Pull Request:

1. Copia el link del PR (la URL de la pagina del Pull Request en GitHub)
2. Envia un mensaje en el **grupo de WhatsApp del curso** con el siguiente formato:

```
Entrega Clase [numero] - [Nombre] [Apellido]
PR: [link al pull request]
```

Ejemplo:

```
Entrega Clase 1 - Juan Perez
PR: https://github.com/perzequiel/curso-ai-engineer/pull/5
```

3. Espera la revision de pares. Un companero revisara tu PR y dejara comentarios si es necesario.

---

## Resumen del flujo completo

```
git fetch --all
git checkout feature/clase-[numero]
git pull origin feature/clase-[numero]
git checkout -b feature/clase-[numero]_[nombre]-[apellido]

# ... completar la consigna hasta que pasen los tests ...

pytest tests/clase_[numero]/ -v

git add .
git commit -m "clase-[numero]: resuelvo tests - [Nombre] [Apellido]"
git push origin feature/clase-[numero]_[nombre]-[apellido]

# Crear PR en GitHub: tu rama -> feature/clase-[numero]
# Avisar en el grupo de WhatsApp
```

---

## Notas importantes

- **NO se realizara merge** del Pull Request. La entrega queda registrada como PR abierto.
- **NO trabajes directamente** sobre la rama `feature/clase-[numero]`. Siempre crea tu rama personal.
- **NO pushees a `main`**. Solo trabaja en tu rama personal.
- Si necesitas corregir algo despues de crear el PR, simplemente hace los cambios, commit y push en la misma rama. El PR se actualiza automaticamente.
- Si tenes dudas, consulta en el grupo de WhatsApp antes de avanzar.
