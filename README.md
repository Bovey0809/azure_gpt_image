# Azure GPT Image Generation & Editing Tool

A web application that leverages Azure OpenAI's image generation capabilities to create and edit images based on text prompts.

## Features

- **Image Generation**: Generate images from text prompts with customizable settings:
  - Multiple size options (1024x1024, 1792x1024, 1024x1792)
  - Quality settings (Standard, Medium, HD)

- **Image Editing**: Modify existing images with natural language instructions:
  - Upload original images for editing
  - Optional mask support to specify areas for editing

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **API**: Azure OpenAI Image Generation API
- **Deployment**: Compatible with Gunicorn for production deployment

## Prerequisites

- Python 3.6+
- An Azure account with access to Azure OpenAI Service
- Azure OpenAI API key with image generation enabled

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd azure_gpt_image
   ```

2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a .env file** in the project root with your Azure API key:
   ```
   AZURE_API_KEY=your_api_key_here
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000/`

## Usage

### Image Generation

1. Enter a detailed text prompt describing the image you want to create
2. Select desired size and quality settings
3. Click "Generate Image" button
4. The generated image will appear below the form

### Image Editing

1. Enter a text prompt describing the edits you want to make
2. Upload the original image (PNG or JPEG format)
3. Optionally upload a mask image (transparent areas will be edited)
4. Click "Edit Image" button
5. The edited image will appear below the form

## Deployment

For production deployment:

```bash
gunicorn app:app
```

## Error Handling

The application includes comprehensive error handling:
- Validation of required inputs
- Detailed error logging for API requests
- User-friendly error messages

## Environment Variables

- `AZURE_API_KEY`: Your Azure OpenAI API key (required)

## Security Notes

- API keys are loaded from environment variables for security
- Error messages to users are sanitized to prevent information leakage

## License

[Your License Information]

---

*Created: April 28, 2025*