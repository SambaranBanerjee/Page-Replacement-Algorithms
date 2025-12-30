# Page-Replacement-Algorithms

An interactive web application that visually demonstrates and compares page replacement algorithms used in Operating Systems. Built for educational purposes to help students understand memory management concepts.

![App Preview](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.3.3-green)
![Vercel](https://img.shields.io/badge/deployed%20on-vercel-black)

## 🌟 Features

### 🎯 Algorithm Visualizations
- **FIFO (First In First Out)**: Visualizes the oldest page replacement strategy
- **LRU (Least Recently Used)**: Shows page replacement based on usage recency
- **Optimal Algorithm**: Demonstrates the theoretical best-case scenario

### 📊 Interactive Features
- **Step-by-Step Execution**: Watch algorithms execute one step at a time
- **Real-time Comparison**: Compare algorithm performance side-by-side
- **Visual Page Tables**: See memory frames update in real-time
- **Interactive Charts**: Bar graphs comparing page fault counts
- **Detailed Statistics**: Hit/miss rates, fault percentages, and performance metrics

### 🎨 User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark/Light Theme**: Clean, modern interface with gradient accents
- **Sample Inputs**: Pre-loaded examples for quick demonstration
- **Random Generator**: Generate random reference strings for testing
- **Download Results**: Export graphs and data for reports

## 🚀 Live Demo

**Demo**:[https://page-replacement-algorithms-alpha.vercel.app/](https://page-replacement-algorithms-alpha.vercel.app/)

## 📋 Prerequisites

- Python 3.8+
- Node.js (for development)
- Modern web browser

## 🏗️ Project Structure

```
page-fault-visualizer/
│
├── backend/                    # Flask Backend
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── algorithms/            # Algorithm implementations
│   │   ├── FIFO.py
│   │   ├── LRU.py
│   │   └── Optimal.py
│   └── plot.py               # Graph generation
│
├── frontend/                  # Frontend Files
│   ├── index.html            # Main HTML file
│   ├── script.js             # Frontend JavaScript
│   ├── style.css             # Styling
│   └── assets/               # Images/icons
│
├── docs/                      # Documentation
│   ├── API.md                # API documentation
│   └── ALGORITHMS.md         # Algorithm explanations
│
├── vercel.json              # Vercel deployment config
└── README.md                # This file
```

## 🔧 API Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/calculate` | POST | Calculate page faults | `frames`, `reference_string`, `algorithms[]` |
| `/api/step-by-step` | POST | Get detailed execution steps | `frames`, `reference_string`, `algorithm` |

### Example API Request

```json
POST /api/calculate
{
  "frames": 3,
  "reference_string": "7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1",
  "algorithms": ["fifo", "lru", "optimal"]
}
```

## 🎮 Usage Guide

### 1. Input Parameters
- **Number of Frames**: Enter the available memory frames (1-10)
- **Reference String**: Space-separated page numbers (e.g., "7 0 1 2 0 3")
- **Algorithms**: Select which algorithms to compare

### 2. Visualization Controls
- **Step Navigation**: Move through algorithm execution step-by-step
- **Play/Pause**: Auto-play through all steps
- **Speed Control**: Adjust visualization speed (Fast/Medium/Slow)

### 3. Understanding the Output
- **Page Table**: Shows frame contents at each step
- **Color Coding**: 
  - 🟢 Green: Page Hit (page found in memory)
  - 🔴 Red: Page Fault (page not in memory)
- **Statistics**: Hit ratio, fault rate, total pages processed
- **Comparison Chart**: Visual comparison of algorithm performance

## 📈 Algorithm Details

### FIFO (First In First Out)
- **Concept**: Replace the oldest page in memory
- **Complexity**: O(n)
- **Advantages**: Simple implementation, low overhead
- **Disadvantages**: Poor performance, suffers from Belady's Anomaly

### LRU (Least Recently Used)
- **Concept**: Replace the least recently used page
- **Complexity**: O(n) with proper implementation
- **Advantages**: Better performance than FIFO, widely used
- **Disadvantages**: Requires additional data structures

### Optimal Algorithm
- **Concept**: Replace the page that won't be used for longest time
- **Complexity**: O(n²)
- **Advantages**: Minimal page faults (theoretical best)
- **Disadvantages**: Not practical (requires future knowledge)

## 🚀 Deployment

### Frontend Deployment (Vercel)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

## 📚 Educational Value

This project helps students understand:
- Page replacement concepts in OS
- Algorithm trade-offs and performance
- Memory management strategies
- Real-world algorithm implementation
- Data visualization techniques

## 🛡️ Security

- CORS properly configured for production
- Input validation on server-side
- No sensitive data storage
- HTTPS enforced in production
- Rate limiting on API endpoints

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Operating System concepts based on standard textbooks
- UI inspiration from modern educational tools
- Chart.js for visualization components
- Flask community for backend framework
- Vercel for hosting services

## 📞 Support

For issues, questions, or contributions:
1. Check [Existing Issues](https://github.com/your-username/page-fault-visualizer/issues)
2. Create [New Issue](https://github.com/your-username/page-fault-visualizer/issues/new)
3. Email: team@pagefaultvisualizer.com

## 🎯 Future Enhancements

- [ ] Add more algorithms (LFU, MRU, Clock)
- [ ] Implement algorithm prediction
- [ ] Add collaborative mode
- [ ] Create downloadable reports
- [ ] Add voice-guided explanations
- [ ] Mobile app version
- [ ] Dark/light theme toggle
- [ ] Internationalization support
- [ ] Performance benchmarking
- [ ] Algorithm animation export

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📊 Performance Metrics

| Algorithm | Average Fault Rate | Best Use Case | Worst Case |
|-----------|-------------------|---------------|------------|
| FIFO | 45-55% | Simple systems | Increasing frames paradox |
| LRU | 35-45% | General purpose | High frequency changes |
| Optimal | 25-35% | Benchmarking | Impractical for real use |

---

<div align="center">
  
**Made with ❤️ by Our OS Project Team**  
*Understanding Memory Management, One Page at a Time*

[Report Bug](https://github.com/your-username/page-fault-visualizer/issues) · 
[Request Feature](https://github.com/your-username/page-fault-visualizer/issues) · 
[View Demo](https://page-fault-visualizer.vercel.app)

</div>

## 📝 Quick Start Commands

```bash
# Clone and run locally
git clone https://github.com/your-username/page-fault-visualizer.git
cd page-fault-visualizer/backend
pip install -r requirements.txt
python app.py

# Open in browser: http://localhost:5000
```
