<html>
  <div id="top" class="">
#update
<div align="center" class="text-center">
<h1>PARKING-MANAGEMENT-PROJECT</h1>
<p><em>Empowering Parking Management, Simplifying Vehicle Check-In/Out Effortlessly</em></p>

<img alt="last-commit" src="https://img.shields.io/github/last-commit/YourUsername/parking-management-project?style=flat&logo=git&logoColor=white&color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="repo-top-language" src="https://img.shields.io/github/languages/top/YourUsername/parking-management-project?style=flat&color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="repo-language-count" src="https://img.shields.io/github/languages/count/YourUsername/parking-management-project?style=flat&color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
<p><em>Built with the tools and technologies:</em></p>
<img alt="Python" src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=python&logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-005571.svg?style=flat&logo=fastapi&logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="MySQL" src="https://img.shields.io/badge/MySQL-4479A1.svg?style=flat&logo=mysql&logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="React" src="https://img.shields.io/badge/React-61DAFB.svg?style=flat&logo=react&logoColor=black" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6.svg?style=flat&logo=typescript&logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="Vite" src="https://img.shields.io/badge/Vite-646CFF.svg?style=flat&logo=vite&logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="Tailwind CSS" src="https://img.shields.io/badge/Tailwind_CSS-38B2AC.svg?style=flat&logo=tailwind-css&logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="npm" src="https://img.shields.io/badge/npm-CB3837.svg?style=flat&logo=npm&logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="Docker" src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=docker&logoColor=white" class="inline-block mx-1" style="margin: 0px 2px;">
</div>
<br>
<hr>
<h2>Table of Contents</h2>
<ul class="list-disc pl-4 my-0">
  <li class="my-0"><a href="#overview">Overview</a></li>
  <li class="my-0"><a href="#getting-started">Getting Started</a>
    <ul class="list-disc pl-4 my-0">
      <li class="my-0"><a href="#prerequisites">Prerequisites</a></li>
      <li class="my-0"><a href="#installation">Installation</a></li>
      <li class="my-0"><a href="#usage">Usage</a></li>
      <li class="my-0"><a href="#testing">Testing</a></li>
    </ul>
  </li>
</ul>
<hr>
<h2 id="overview">Overview</h2>
<p>
  <strong>Parking Management Project</strong> is a full-stack solution for automating vehicle check-in/check-out, license plate recognition, and fee calculation in parking facilities.
</p>
<p><strong>Why Parking Management?</strong></p>
<ul class="list-disc pl-4 my-0">
  <li class="my-0">🚗 <strong>Automated Entry/Exit:</strong> RFID & OCR-powered workflow for seamless vehicle access.</li>
  <li class="my-0">🎥 <strong>Live Supervision:</strong> RTSP camera integration with real-time streaming.</li>
  <li class="my-0">💰 <strong>Dynamic Fee Calculation:</strong> Configurable rate rules and zone management.</li>
  <li class="my-0">📊 <strong>Detailed Reporting:</strong> CSV export and revenue charts by day/week/month.</li>
  <li class="my-0">👥 <strong>User Management:</strong> Role-based access for Admin and Staff.</li>
</ul>
<hr>
<h2 id="getting-started">Getting Started</h2>
<h3 id="prerequisites">Prerequisites</h3>
<p>This project requires:</p>
<ul class="list-disc pl-4 my-0">
  <li class="my-0"><strong>Backend:</strong> Python ≥3.7</li>
  <li class="my-0"><strong>Frontend:</strong> Node.js & npm</li>
  <li class="my-0"><strong>Database:</strong> MySQL Server</li>
  <li class="my-0"><strong>Container Runtime:</strong> Docker (optional)</li>
</ul>
<h3 id="installation">Installation</h3>
<ol class="list-decimal pl-4 my-0">
  <li class="my-0"><strong>Clone the repository:</strong>
    <pre><code class="language-sh">git clone https://github.com/YourUsername/parking-management-project.git
cd parking-management-project
</code></pre>
  </li>
  <li class="my-0"><strong>Backend setup:</strong>
    <pre><code class="language-sh">cd backend
pip install -r requirements.txt
</code></pre>
  </li>
  <li class="my-0"><strong>Frontend setup:</strong>
    <pre><code class="language-sh">cd ../frontend
npm install
</code></pre>
  </li>
  <li class="my-0"><strong>Environment variables:</strong> Create a <code>.env</code> in <code>backend/</code>:
    <pre><code class="language-sh">DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=your_password
CAM_RTSP_URL=rtsp://user:pass@ip:554/stream
</code></pre>
  </li>
</ol>
<p><strong>Using Docker Compose:</strong></p>
<pre><code class="language-sh">docker-compose up --build
</code></pre>
<h3 id="usage">Usage</h3>
<p>Start the services:</p>
<ul class="list-disc pl-4 my-0">
  <li class="my-0"><strong>Manual:</strong>
    <pre><code class="language-sh"># In backend/
uvicorn main:app --reload  
# In frontend/
npm run dev
</code></pre>
  </li>
  <li class="my-0"><strong>Docker:</strong>
    <pre><code class="language-sh">docker-compose up
</code></pre>
  </li>
</ul>
<h3 id="testing">Testing</h3>
<p>Run the test suites:</p>
<ul class="list-disc pl-4 my-0">
  <li class="my-0"><strong>Backend (pytest):</strong>
    <pre><code class="language-sh">cd backend
pytest
</code></pre>
  </li>
  <li class="my-0"><strong>Frontend (Jest):</strong>
    <pre><code class="language-sh">cd frontend
npm test
</code></pre>
  </li>
</ul>
<hr>
<div align="left" class=""><a href="#top">⬆ Return</a></div>
<hr>
</div>
</html>
