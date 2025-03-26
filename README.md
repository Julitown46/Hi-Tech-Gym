# Sistema de Gestión para Gimnasios con Reservas de Pistas de Pádel

## Título
Hi-Tech Gym

## Descripción
Este proyecto es una plataforma web desarrollada con **Spring Boot, JPA, SQL y Angular** que permite la gestión integral de un gimnasio, incluyendo la administración de usuarios, membresías y reservas de pistas de pádel.

## Objetivos
- Facilitar la gestión de gimnasios mediante una solución digital eficiente.
- Permitir a los usuarios reservar pistas de pádel de forma intuitiva.
- Automatizar la administración de membresías y pagos.
- Proporcionar un panel de control para administradores con estadísticas.

## Tecnologías Utilizadas
- **Backend:** Spring Boot, JPA, Hibernate, MySQL
- **Frontend:** Angular 19, Bootstrap
- **Base de Datos:** MySQL
- **Seguridad:** Spring Security (Autenticación y Autorización)

## Funcionalidades Principales
### Para Usuarios
- Registro e inicio de sesión.
- Reservar pistas de pádel (solo si tienen una membresía activa).
- Ver su historial de reservas y estado de su membresía.

### Para Administradores
- Gestionar usuarios y membresías.
- Administrar reservas de pistas de pádel.
- Ver estadísticas del gimnasio.

## Requisitos
### Software Necesario
- Java 17+
- Node.js y Angular CLI
- MySQL Server
- Spring Boot

### Configuración de la Base de Datos
Ejecuta el siguiente script SQL para crear la base de datos y las tablas necesarias:

```sql
CREATE DATABASE HiTechGym;
USE HiTechGym;
```
_(Para ver el script completo, revisa `DDBBHiTechGym.sql` en este repositorio)_

## Instalación y Ejecución
### 1. Clonar el repositorio
```sh
git clone https://github.com/tu-usuario/sistema-gimnasio.git
cd sistema-gimnasio
```

### 2. Configurar el Backend (Spring Boot)
```sh
cd backend
mvn clean install
mvn spring-boot:run
```

### 3. Configurar el Frontend (Angular)
```sh
cd frontend
npm install
ng serve
```

## Notas Importantes
- Solo los usuarios con **membresía activa** pueden reservar pistas de pádel.
- El sistema implementa validaciones tanto en el **backend (Spring Boot)** como en la **base de datos (Triggers en MySQL)**.
- Se recomienda usar Postman para probar la API antes de integrar el frontend.

## Licencia
Este proyecto está bajo la licencia MIT. Puedes usarlo y modificarlo libremente.

---
**Desarrollado por:** Julián Moreno Cuenca 🚀

