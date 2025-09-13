from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.dependencies import get_access_token, AccessToken
from jose import jwt
import os

# Local imports
from database import NoteRepository

# Load environment variables from .env file
load_dotenv()

# Configure OAuth2 Bearer token authentication using Stytch
# This validates JWT tokens issued by Stytch for secure API access
auth = BearerAuthProvider(
    jwks_uri=f"{os.getenv('STYTCH_DOMAIN')}/.well-known/jwks.json",
    issuer=os.getenv("STYTCH_DOMAIN"),
    algorithm="RS256",
    audience=os.getenv("STYTCH_PROJECT_ID"),
)

# Initialize the FastMCP server with authentication
mcp = FastMCP(name="Notes App", auth=auth)

@mcp.tool()
def get_my_notes() -> str:
    """
    Retrieve all notes belonging to the authenticated user.

    This function extracts the user ID from the JWT access token and fetches
    all notes associated with that user from the database. The notes are
    returned in a formatted string for easy reading.

    Returns:
        str: A formatted string containing all user notes, or "no notes found"
             if the user has no notes.

    Raises:
        Exception: If there's an issue with token validation or database access.
    """
    # Extract user ID from the JWT access token
    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token)["sub"]

    # Fetch all notes for the authenticated user
    notes = NoteRepository.get_notes_by_user(user_id)

    # Handle case where no notes exist
    if not notes:
        return "no notes found"

    # Format notes for display
    result = "Your notes:\n"
    for note in notes:
        result += f"{note.id}: {note.content}\n"

    return result


@mcp.tool()
def add_note(content: str) -> str:
    """
    Create a new note for the authenticated user.

    This function creates a new note with the provided content and associates
    it with the authenticated user. The note is stored in the database and
    a confirmation message is returned.

    Args:
        content (str): The text content of the note to be created.

    Returns:
        str: A confirmation message indicating the note was successfully added
             with the note content.

    Raises:
        Exception: If there's an issue with token validation or database access.
    """
    # Extract user ID from the JWT access token
    access_token: AccessToken = get_access_token()
    user_id = jwt.get_unverified_claims(access_token.token)["sub"]

    # Create the note in the database
    note = NoteRepository.create_note(user_id, content)

    # Return confirmation with note details
    return f"added note: {note.content}"

@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET", "OPTIONS"])
def oauth_metadata(request: StarletteRequest) -> JSONResponse:
    """
    Provide OAuth2 protected resource metadata for client discovery.

    This endpoint implements the OAuth2 Protected Resource Metadata specification,
    allowing OAuth2 clients to discover information about this protected resource
    server, including supported scopes and authentication methods.

    Args:
        request (StarletteRequest): The incoming HTTP request.

    Returns:
        JSONResponse: OAuth2 metadata including:
            - resource: The base URL of this resource server
            - authorization_servers: List of authorization server URLs
            - scopes_supported: Supported OAuth2 scopes
            - bearer_methods_supported: Supported bearer token methods
    """
    # Extract base URL from the request
    base_url = str(request.base_url).rstrip("/")

    # Return OAuth2 metadata in the standard format
    return JSONResponse(
        {
            "resource": base_url,
            "authorization_servers": [os.getenv("STYTCH_DOMAIN")],
            "scopes_supported": ["read", "write"],
            "bearer_methods_supported": ["header", "body"],
        }
    )

if __name__ == "__main__":
    """
    Main entry point for the MCP server.

    This block configures and starts the FastMCP server with:
    - HTTP transport on localhost:8000
    - CORS middleware for cross-origin requests
    - OAuth2 authentication via Stytch
    """
    mcp.run(
        transport="http",  # Use HTTP transport for web compatibility
        host="127.0.0.1",  # Listen on localhost
        port=8000,  # Standard port for development
        middleware=[
            # Configure CORS middleware for web client support
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],  # Allow all origins (configure for production)
                allow_credentials=True,  # Allow credentials for authentication
                allow_methods=["*"],  # Allow all HTTP methods
                allow_headers=["*"],  # Allow all headers
            )
        ],
    )
