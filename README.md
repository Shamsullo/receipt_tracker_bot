# Receipt Tracking Telegram Bot

A comprehensive Telegram bot for tracking and analyzing receipts with OCR capabilities, team collaboration, and financial analytics.

## 🎯 Project Overview

This Telegram bot allows users to upload receipt images/PDFs, automatically extracts financial data using OCR (Optical Character Recognition), and provides analytics on spending patterns, sources, and account transactions. The system supports team collaboration where multiple users can contribute receipts to shared analytics.

### Key Features

- **📱 Telegram Bot Interface**: Easy-to-use bot commands for receipt management
- **🔍 OCR Processing**: Automatic extraction of receipt data (amount, date, sender, receiver, etc.)
- **👥 Team Collaboration**: Multi-user teams with admin controls
- **📊 Analytics**: Period-based receipt analysis and spending insights
- **💾 File Storage**: Secure storage of receipt images/PDFs
- **🔐 Authentication**: User authentication and team-based access control
- **📈 Financial Tracking**: Track total amounts, sources, and transaction patterns

## 🏗️ Architecture

### Technology Stack

- **Backend**: Python 3.8+
- **Bot Framework**: aiogram 2.25+
- **Database**: SQLAlchemy with PostgreSQL/SQLite
- **OCR**: Tesseract with pytesseract
- **File Processing**: Pillow, pdf2image, pdfplumber
- **Async Support**: asyncio, aiofiles

### Project Structure

```
PythonProject/
├── app/
│   ├── bot/                    # Telegram bot handlers and middleware
│   │   ├── handlers/           # Command handlers
│   │   └── middlewares/        # Authentication middleware
│   ├── core/                   # Core configuration and utilities
│   ├── db/                     # Database models and migrations
│   ├── models/                 # SQLAlchemy models
│   ├── repositories/           # Data access layer
│   ├── services/               # Business logic layer
│   │   ├── ocr/               # OCR processing services
│   │   └── interfaces/        # Service interfaces
│   └── __init__.py
├── alembic/                    # Database migrations
├── uploads/                    # Receipt file storage
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR engine
- PostgreSQL (recommended) or SQLite
- Telegram Bot Token

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PythonProject
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   
   **macOS:**
   ```bash
   brew install tesseract
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get install tesseract-ocr
   ```
   
   **Windows:**
   Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/receipt_bot
   UPLOAD_DIR=uploads
   OCR_ENABLED=true
   TESSERACT_CMD=/usr/local/bin/tesseract
   ```

5. **Initialize database**
   ```bash
   alembic upgrade head
   ```

6. **Run the bot**
   ```bash
   python main.py
   ```

## 📱 Bot Usage

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize bot and welcome message | `/start` |
| `/upload_receipt` | Upload a receipt image/PDF | `/upload_receipt` + attach file |
| `/list_receipts` | List receipts for a date range | `/list_receipts 2024-01-01 2024-01-31` |
| `/create_team` | Create a new team | `/create_team MyTeam` |
| `/join_team` | Join an existing team | `/join_team team_invite_link` |
| `/team_info` | View team information | `/team_info` |

### Workflow

1. **User Registration**: Users start the bot and are automatically registered
2. **Team Setup**: Users create or join teams for collaborative receipt tracking
3. **Receipt Upload**: Users upload receipt images/PDFs using `/upload_receipt`
4. **OCR Processing**: Bot automatically extracts data using OCR
5. **Data Storage**: Receipt data is stored in the database with file backup
6. **Analytics**: Users can query receipts by date range and view summaries

## 🗄️ Database Schema

### Core Tables

#### Users
- `id`: Primary key
- `telegram_id`: Telegram user ID
- `username`: Telegram username

#### Teams
- `id`: Primary key
- `name`: Team name (unique)

#### Team Members
- `id`: Primary key
- `team_id`: Foreign key to teams
- `user_id`: Foreign key to users
- `is_admin`: Admin privileges flag

#### Receipts
- `id`: Primary key
- `team_id`: Associated team
- `uploaded_by`: User who uploaded
- `date`: Receipt date
- `amount`: Transaction amount
- `operation_number`: Bank operation number
- `sender`: Sender account/organization
- `receiver`: Receiver account/organization
- `status`: Receipt status (pending, approved, rejected)
- `file_path`: Path to stored file
- `organization`: Organization name
- `fee`: Transaction fee
- `notes`: Additional notes
- `creation_at`: Upload timestamp

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BOT_TOKEN` | Telegram bot token | Required |
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./app.db` |
| `UPLOAD_DIR` | Receipt file storage directory | `uploads` |
| `MAX_FILE_SIZE` | Maximum file size (bytes) | `20971520` (20MB) |
| `OCR_ENABLED` | Enable OCR processing | `true` |
| `TESSERACT_CMD` | Tesseract executable path | Auto-detected |
| `MAX_RECEIPTS_PER_PAGE` | Receipts per page in listings | `5` |
| `MAX_TEAM_MEMBERS` | Maximum team members | `10` |

### OCR Configuration

The bot uses Tesseract OCR to extract text from receipt images. Supported formats:
- **Images**: JPEG, PNG
- **Documents**: PDF

Extracted data includes:
- Transaction amount
- Date
- Operation number
- Sender/receiver information
- Organization name
- Transaction fees

## 📊 Analytics Features

### Receipt Analysis

The bot provides comprehensive analytics on uploaded receipts:

1. **Period-based Summaries**
   - Total receipts in date range
   - Total amount spent
   - Average transaction amount
   - Receipt count by status

2. **Source Analysis**
   - Top sending organizations
   - Top receiving accounts
   - Transaction patterns by source

3. **Team Analytics**
   - Team spending overview
   - Member contribution statistics
   - Shared financial insights

### Example Analytics Output

```
Receipts for period: 2024-01-01 to 2024-01-31
Total receipts: 15
Total amount: 2,450.75
Average amount: 163.38

Receipt 123: 2024-01-15 - Amount: 150.00 - Status: approved
Receipt 124: 2024-01-18 - Amount: 75.50 - Status: pending
...
```

## 🔐 Security & Permissions

### Authentication
- Users are authenticated via Telegram ID
- Session-based authentication with middleware
- Automatic user registration on first interaction

### Team Permissions
- **Team Admins**: Can approve/reject receipts, manage team members
- **Team Members**: Can upload receipts, view team analytics
- **Invite System**: Secure team invitation links with expiration

### File Security
- File type validation (images/PDFs only)
- File size limits (20MB max)
- Secure file storage with unique naming
- Access control through team membership

## 🛠️ Development

### Running in Development

1. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure development settings**
   ```env
   DB_ECHO=true
   OCR_ENABLED=true
   ```

3. **Run with hot reload**
   ```bash
   python main.py
   ```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/
```

## 🚀 Deployment

### Docker Deployment

1. **Build image**
   ```bash
   docker build -t receipt-bot .
   ```

2. **Run container**
   ```bash
   docker run -d \
     --name receipt-bot \
     -e BOT_TOKEN=your_token \
     -e DATABASE_URL=postgresql://... \
     receipt-bot
   ```

### Production Considerations

- Use PostgreSQL for production database
- Set up proper logging and monitoring
- Configure backup strategies for receipt files
- Use environment-specific configuration
- Set up SSL/TLS for secure communications

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request


## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation for common issues

## 🔮 Future Enhancements

- **Advanced Analytics**: Machine learning for spending pattern analysis
- **Export Features**: PDF/Excel report generation
- **Multi-language Support**: Internationalization
- **Mobile App**: Native mobile application
- **API Integration**: REST API for external integrations
- **Real-time Notifications**: Push notifications for receipt updates
- **Budget Tracking**: Budget limits and alerts
- **Receipt Categories**: Automatic categorization of receipts 