# CloudPhotoTransfer 📸

CloudPhotoTransfer is a professional desktop application built with Python and PyQt6 designed to download large volumes of photos from Google Cloud Storage (GCS) buckets efficiently and securely.

![Main Interface Placeholder](https://via.placeholder.com/800x450.png?text=CloudPhotoTransfer+UI+Screenshot)

## ✨ Features

- **High-Speed Downloads**: Optimized for handling 50GB+ of photographic data.
- **Real-time Progress**: Visual tracking of download speed, file count, and byte progress.
- **Modern UI**: Sleek dark-mode interface built with custom QSS styling.
- **Reliability**: Automatic verification of disk space and detailed transfer logging.
- **Security**: Built-in support for Service Account authentication with secure credential handling.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google Cloud Platform account with a Storage Bucket.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/CloudPhotoTransfer.git
   cd CloudPhotoTransfer
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 🔑 Google Cloud Setup

To use this application, you need to provide your own Google Cloud Service Account credentials:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **IAM & Admin > Service Accounts**.
3. Create a Service Account or use an existing one with **Storage Object Viewer** permissions.
4. Generate a new **JSON Key** and download it.
5. Rename the file to `credentials.json` and place it in the root directory of this project.

> [!CAUTION]
> **Never share your `credentials.json` file.** This project includes it in `.gitignore` by default to prevent accidental uploads to GitHub.

---

## 🛠️ Project Structure

```text
CloudPhotoTransfer/
├── assets/             # Icons and visual assets
├── logic/              # Core business logic (GCS downloader)
├── ui/                 # UI components and QSS stylesheets
├── tests/              # Automated tests
├── main.py             # Application entry point
├── build.py            # Executable build script (PyInstaller)
├── credentials.json.example  # Mockup for credentials setup
└── .gitignore          # Safeguard for private data
```

## 📦 Building the App

To create a standalone `.exe` for Windows:
```bash
python build.py
```
Check the `dist/` directory for the final application.

---

## 🇪🇸 Descripción en Español

**CloudPhotoTransfer** es una aplicación de escritorio profesional desarrollada en Python con PyQt6 para la descarga masiva de fotos desde buckets de Google Cloud Storage.

### Características Principales:
- **Descargas Masivas**: Diseñado para mover volúmenes de datos superiores a 50GB.
- **Interfaz Moderna**: Estética "dark mode" con micro-animaciones y barras de progreso en tiempo real.
- **Seguridad**: Gestión segura de credenciales mediante Cuentas de Servicio de GCP.
- **Soporte Offline**: Generación de logs locales para verificar cada archivo descargado.

> [!NOTE]
> Para utilizar esta aplicación, deberás renombrar tu archivo de credenciales de Google Cloud a `credentials.json` y colocarlo en la raíz del proyecto.

---

## 📽️ Demo Video
[Link to Video Placeholder]

## 🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License
This project is licensed under the MIT License.
