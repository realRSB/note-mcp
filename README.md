# Pro-MCP: Secure Notes Application

A full-stack notes application built with the Model Context Protocol (MCP) that provides secure, authenticated note-taking capabilities. The application features a Python FastMCP backend with OAuth2 authentication via Stytch and a React frontend for user interaction.

## 🚀 Features

- **Secure Authentication**: OAuth2 Bearer token authentication using Stytch
- **Note Management**: Create, retrieve, and manage personal notes
- **User Isolation**: Each user can only access their own notes
- **MCP Integration**: Built on FastMCP for seamless AI assistant integration
- **Modern Frontend**: React-based user interface with Vite build system
- **Database Persistence**: SQLite database with SQLAlchemy ORM
- **CORS Support**: Cross-origin resource sharing for web client compatibility

## 🏗️ Architecture

### Backend (Python/FastMCP)
- **Framework**: FastMCP with HTTP transport
- **Authentication**: Stytch OAuth2 with JWT validation
- **Database**: SQLite with SQLAlchemy ORM
- **Port**: 8000 (localhost)

### Frontend (React)
- **Framework**: React 19 with Vite
- **Authentication**: Stytch React SDK
- **Build Tool**: Vite for fast development and building
- **Styling**: CSS with modern development setup

## 📁 Project Structure

```
pro-mcp/
├── backend/
│   ├── main.py              # FastMCP server with authentication
│   ├── database.py          # SQLAlchemy models and repository
│   ├── pyproject.toml       # Python dependencies
│   └── README.md           # This file
└── frontend/
    ├── src/
    │   ├── App.jsx          # Main React component
    │   ├── main.jsx         # React entry point
    │   └── App.css          # Application styles
    ├── package.json         # Node.js dependencies
    ├── vite.config.js       # Vite configuration
    └── index.html           # HTML template
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.13+
- Node.js 18+
- Stytch account for authentication

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -e .
   ```

3. Create a `.env` file with your Stytch credentials:
   ```env
   STYTCH_DOMAIN=your-stytch-domain
   STYTCH_PROJECT_ID=your-project-id
   ```

4. Run the backend server:
   ```bash
   python main.py
   ```

The backend will start on `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## 🔧 API Endpoints

### MCP Tools

#### `get_my_notes()`
Retrieves all notes belonging to the authenticated user.

**Returns**: Formatted string containing all user notes

#### `add_note(content: str)`
Creates a new note for the authenticated user.

**Parameters**:
- `content` (str): The text content of the note

**Returns**: Confirmation message with note content

### OAuth2 Metadata

#### `/.well-known/oauth-protected-resource`
Provides OAuth2 protected resource metadata for client discovery.

**Returns**: JSON metadata including supported scopes and authentication methods

## 🔐 Authentication

The application uses Stytch for OAuth2 authentication:

- **JWT Validation**: RS256 algorithm with JWKS endpoint
- **Scopes**: `read` and `write` permissions
- **Bearer Methods**: Header and body token support
- **User Isolation**: Each user's notes are isolated by user ID from JWT claims

## 🗄️ Database Schema

### Notes Table
- `id`: Primary key (Integer)
- `user_id`: User identifier (String, indexed)
- `content`: Note content (Text)
- `title`: Optional note title (String, indexed)
- `category`: Optional category (String, indexed)
- `tags`: JSON string of tags (Text)
- `is_archived`: Soft delete flag (Boolean, indexed)
- `is_pinned`: Important note flag (Boolean, indexed)
- `created_at`: Creation timestamp (DateTime, indexed)
- `updated_at`: Last modification timestamp (DateTime, indexed)

## 🚀 Development

### Backend Development
- The FastMCP server runs with CORS enabled for development
- Database is automatically created on first run
- JWT tokens are validated on each request

### Frontend Development
- Hot module replacement with Vite
- ESLint configuration for code quality
- React 19 with modern hooks and features

## 🔒 Security Features

- **JWT Token Validation**: All requests require valid JWT tokens
- **User Isolation**: Users can only access their own notes
- **CORS Configuration**: Configurable cross-origin policies
- **OAuth2 Compliance**: Standard OAuth2 protected resource implementation

## 📝 Usage

1. **Authentication**: Users authenticate through the Stytch login interface
2. **Note Creation**: Use the `add_note` MCP tool to create new notes
3. **Note Retrieval**: Use the `get_my_notes` MCP tool to view all notes
4. **AI Integration**: The MCP tools can be used by AI assistants for note management

## 🛠️ Technologies Used

### Backend
- **FastMCP**: Model Context Protocol server framework
- **SQLAlchemy**: Python ORM for database operations
- **Stytch**: Authentication and user management
- **python-jose**: JWT token handling
- **Starlette**: ASGI framework for HTTP handling

### Frontend
- **React 19**: Modern React with latest features
- **Vite**: Fast build tool and development server
- **Stytch React SDK**: Authentication integration
- **ESLint**: Code linting and quality assurance


