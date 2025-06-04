# Proyecto Parcial Clara Mitre - Gestión de Libros y Autores

Este proyecto es una aplicación de consola desarrollada en Java que permite gestionar libros y autores en una base de datos relacional utilizando JDBC y H2. Implementa el patrón DAO y está estructurado en capas para separar la lógica de negocio del acceso a datos.

## Requisitos del sistema

- Java 17 o superior
- Gradle
- IntelliJ IDEA (recomendado)

## Ruta del GitHub

2doCuatri > Prog2 > Programacion2 > Mie > Parcial > src > main > java > org > example

## Estructura del proyecto

```
src/
├── main/
│   ├── java/
│   │   ├── main/               → Clase Main
│   │   ├── model/              → Clases de dominio: `Autor`, `Libro`
│   │   ├── dao/                → Interfaces DAO
│   │   └── util/               → Conexión a la base de datos
│       └── log.xml             → Configuración de Log4j
```

## Archivos importantes

- build.gradle
- settings.gradle
- log.xml
- carpeta dao: AutorDAO, AutorDAOImpl, GenericDAO, LibroDAO, LibroDAOImpl
- carpeta main: main
- carpeta util: DataBaseUtil
- carpeta model: Libro, Autor

## Funcionalidades

- Crear y listar autores
- Crear y listar libros
- Registrar si un libro está disponible
- Asociar libros a autores mediante `autor_id`
- Persistencia automática en base de datos H2
- Logging con Log4j
- Tablas creadas automáticamente desde Java

## Base de datos

- Motor: **H2**
