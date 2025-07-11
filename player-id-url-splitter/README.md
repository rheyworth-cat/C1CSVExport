# Player ID URL Splitter

A Streamlit web application that splits URLs containing multiple player IDs into two separate URLs for easier CSV export.

## Features

- Split URLs with `playerIDs` parameter into two equal parts
- User-friendly web interface
- One-click URL opening for CSV export
- Error handling and validation
- Responsive design

## How to Use

1. Visit the deployed app
2. Paste your URL containing `playerIDs` parameter
3. Click "Split URL" 
4. Use the generated URLs to export CSV files

## Local Development

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/player-id-url-splitter.git
cd player-id-url-splitter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

4. Open your browser and go to `http://localhost:8501`

## Deployment

This app can be deployed on:
- Streamlit Cloud (recommended)
- Heroku
- Railway
- Any cloud platform supporting Python

### Streamlit Cloud Deployment

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy!

## URL Format

The application expects URLs in this format:
```
https://example.com/data?playerIDs=player1%2Cplayer2%2Cplayer3%2Cplayer4&other=params
```

This will be split into:
- URL A: `https://example.com/data?playerIDs=player1%2Cplayer2&other=params`
- URL B: `https://example.com/data?playerIDs=player3%2Cplayer4&other=params`

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License