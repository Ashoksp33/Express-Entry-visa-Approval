/* 
   INTERACTIVE REST API SIMULATOR MODAL
   Showcases Ashok Gowda's Spring Boot REST API Architecture Live!
*/

class RestApiSimulator {
  constructor() {
    this.modalOverlay = document.getElementById('api-modal-overlay');
    this.modalClose = document.getElementById('modal-close-btn');
    this.urlDisplay = document.getElementById('api-url-display');
    this.methodDisplay = document.getElementById('api-method-badge');
    this.responseCode = document.getElementById('api-status-code');
    this.responseBody = document.getElementById('api-response-body');

    this.mockDatabase = [
      { id: 1, name: 'Ashok Gowda S P', role: 'Backend Software Engineer', department: 'Engineering', tech: 'Spring Boot, MySQL', salary: 120000 },
      { id: 2, name: 'Cyber Agent Alpha', role: 'Security Architect', department: 'CyberOps', tech: 'OAuth2, JWT', salary: 110000 },
      { id: 3, name: 'Data Specialist', role: 'ML Engineer', department: 'AI Core', tech: 'Python, Flask, LSTM', salary: 115000 }
    ];

    if (this.modalOverlay) this.init();
  }

  init() {
    document.querySelectorAll('.trigger-api-modal').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        if (window.cyberAudio) window.cyberAudio.playClickSFX();
        this.openModal();
      });
    });

    if (this.modalClose) {
      this.modalClose.addEventListener('click', () => this.closeModal());
    }

    this.modalOverlay.addEventListener('click', (e) => {
      if (e.target === this.modalOverlay) this.closeModal();
    });

    // Endpoint buttons inside modal
    document.querySelectorAll('.api-endpoint-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const method = btn.getAttribute('data-method');
        const endpoint = btn.getAttribute('data-endpoint');
        if (window.cyberAudio) window.cyberAudio.playClickSFX();
        this.executeRequest(method, endpoint);
      });
    });
  }

  openModal() {
    this.modalOverlay.classList.add('active');
    this.executeRequest('GET', '/api/employees');
  }

  closeModal() {
    this.modalOverlay.classList.remove('active');
  }

  executeRequest(method, endpoint) {
    this.urlDisplay.textContent = `https://api.ashokgowda.dev${endpoint}`;
    this.methodDisplay.textContent = method;

    // Reset method styling
    this.methodDisplay.className = 'tech-badge';
    if (method === 'GET') this.methodDisplay.style.color = '#00ff66';
    if (method === 'POST') this.methodDisplay.style.color = '#00f0ff';
    if (method === 'PUT') this.methodDisplay.style.color = '#ffe600';
    if (method === 'DELETE') this.methodDisplay.style.color = '#ff0055';

    this.responseBody.textContent = '// Executing Spring Boot Controller request...';
    this.responseCode.textContent = 'HTTP 102 PROCESSING';
    this.responseCode.style.color = '#ffe600';

    setTimeout(() => {
      let responseObj = null;
      let status = '200 OK';

      if (endpoint === '/api/employees' && method === 'GET') {
        responseObj = { status: 200, message: 'Employees retrieved successfully', data: this.mockDatabase };
      } else if (endpoint === '/api/employees/1' && method === 'GET') {
        responseObj = { status: 200, message: 'Employee found', data: this.mockDatabase[0] };
      } else if (method === 'POST') {
        const newEmp = { id: 4, name: 'New Engineer', role: 'Full Stack Dev', department: 'Engineering', tech: 'Java, React', salary: 95000 };
        status = '201 CREATED';
        responseObj = { status: 201, message: 'Employee created via Spring Data JPA Hibernate', data: newEmp };
      } else if (method === 'DELETE') {
        status = '200 OK';
        responseObj = { status: 200, message: 'Employee record ID #1 purged from MySQL DB successfully' };
      }

      this.responseCode.textContent = `HTTP ${status}`;
      this.responseCode.style.color = status.includes('201') || status.includes('200') ? '#00ff66' : '#ff0055';
      this.responseBody.textContent = JSON.stringify(responseObj, null, 2);

      if (window.cyberAudio) window.cyberAudio.playSuccessSFX();
    }, 450);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.restApiSimulator = new RestApiSimulator();
});
