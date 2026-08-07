/* 
   EXECUTIVE MIDNIGHT SLATE PORTFOLIO DRIVER
   Developer: Ashok Gowda S P
*/

document.addEventListener('DOMContentLoaded', () => {
  // 1. Scroll Reveal Observer
  initScrollReveal();

  // 2. Tech Filter Tabs
  initTechTabs();

  // 3. Dynamic Multi-Project Architecture Modals
  initArchitectureModals();

  // 4. Contact Form Validation
  initContactForm();

  // 5. Active Nav Highlight on Scroll
  initActiveNav();
});

/* SCROLL REVEAL OBSERVER */
function initScrollReveal() {
  const elements = document.querySelectorAll('.fade-in-up');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  elements.forEach(el => observer.observe(el));
}

/* TECH STACK FILTER TABS */
function initTechTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  const cards = document.querySelectorAll('.tech-card');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const filter = tab.getAttribute('data-filter');

      cards.forEach(card => {
        const cat = card.getAttribute('data-category');
        if (filter === 'all' || cat === filter) {
          card.style.display = 'block';
          card.style.opacity = '1';
        } else {
          card.style.display = 'none';
          card.style.opacity = '0';
        }
      });
    });
  });
}

/* DYNAMIC ARCHITECTURE MODAL SYSTEM */
function initArchitectureModals() {
  const overlay = document.getElementById('arch-modal-overlay');
  const closeBtn = document.getElementById('arch-modal-close');
  const titleEl = document.getElementById('arch-modal-title');
  const descEl = document.getElementById('arch-modal-desc');
  const contentEl = document.getElementById('arch-modal-content');

  if (!overlay) return;

  // Data for architecture breakdowns of each project
  const architectureData = {
    'rest-api': {
      title: 'Spring Boot RESTful Microservice Architecture',
      desc: 'Layered Enterprise Pattern (Controller → Service → Repository → MySQL Database) separating HTTP endpoints, business logic rules, and relational data access.',
      content: `
        <div style="background:#020617; border:1px solid var(--border-subtle); border-radius:var(--radius-md); padding:1.5rem; font-family:var(--font-code); font-size:0.88rem; color:var(--text-primary); line-height:2;">
          <div style="color:var(--accent-cyan); font-weight:700;"><i class="fas fa-desktop"></i> 1. CLIENT / POSTMAN CONSUMER</div>
          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Transmits HTTP Requests (JSON Payload / Headers)</div>

          <div style="color:var(--accent-indigo); font-weight:700;"><i class="fas fa-layer-group"></i> 2. CONTROLLER LAYER (@RestController)</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Exposes Endpoints (/api/employees, /api/employees/{id})<br>
            • Handles Request Body Deserialization & Response Formatting
          </div>

          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Invokes Business Logic Methods</div>

          <div style="color:var(--accent-emerald); font-weight:700;"><i class="fas fa-cogs"></i> 3. SERVICE LAYER (@Service)</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Implements Business Logic & Transactional Scopes<br>
            • Validates Input Parameters & Exception Mapping
          </div>

          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Calls Spring Data JPA Repository Interface</div>

          <div style="color:var(--accent-amber); font-weight:700;"><i class="fas fa-database"></i> 4. DATA ACCESS LAYER (Hibernate ORM / @Repository)</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Executes Prepared Statements via Spring Data JPA<br>
            • Maps Relational Rows to Java Entity Model Classes
          </div>

          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Connection Pool Query Execution (Port 3306)</div>

          <div style="color:var(--accent-cyan); font-weight:700;"><i class="fas fa-server"></i> 5. MYSQL RELATIONAL DATABASE</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Relational Tables with Foreign Keys, Primary Keys, and Indexes
          </div>
        </div>
      `
    },
    'console-system': {
      title: 'Modular Java Core & JDBC Prepared Statements Architecture',
      desc: 'Layered Object-Oriented Console architecture enforcing SQL injection prevention and database transaction integrity.',
      content: `
        <div style="background:#020617; border:1px solid var(--border-subtle); border-radius:var(--radius-md); padding:1.5rem; font-family:var(--font-code); font-size:0.88rem; color:var(--text-primary); line-height:2;">
          <div style="color:var(--accent-cyan); font-weight:700;"><i class="fas fa-terminal"></i> 1. CONSOLE USER INTERFACE ENGINE</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Interactive CLI Scanner Input Loop & Menu Dispatcher
          </div>

          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Dispatches User Choice</div>

          <div style="color:var(--accent-indigo); font-weight:700;"><i class="fas fa-cubes"></i> 2. CORE JAVA OBJECT-ORIENTED MODEL & SERVICE</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Encapsulated Employee Entity (Getters, Setters, Constructor)<br>
            • Custom Exception Handler & Data Validation
          </div>

          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Establishes DriverManager Connection</div>

          <div style="color:var(--accent-emerald); font-weight:700;"><i class="fas fa-link"></i> 3. JDBC PREPARED STATEMENT LAYER</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Safe Dynamic Parameter Binding (? placeholders)<br>
            • Prevents SQL Injection Vulnerabilities Completely
          </div>

          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Executes Query / Update</div>

          <div style="color:var(--accent-amber); font-weight:700;"><i class="fas fa-database"></i> 4. MYSQL DATABASE ENGINE</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Performs Persistent Insert, Select, Update, and Delete Actions
          </div>
        </div>
      `
    },
    'stock-prediction': {
      title: 'Machine Learning Deep Learning Pipeline Architecture',
      desc: 'End-to-end Deep Learning pipeline using LSTM networks for time-series stock trend forecasting served via Flask.',
      content: `
        <div style="background:#020617; border:1px solid var(--border-subtle); border-radius:var(--radius-md); padding:1.5rem; font-family:var(--font-code); font-size:0.88rem; color:var(--text-primary); line-height:2;">
          <div style="color:var(--accent-cyan); font-weight:700;"><i class="fas fa-file-csv"></i> 1. HISTORICAL DATA INGESTION</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Ingests Stock Price Time-Series Data via Yahoo Finance API / Pandas
          </div>

          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Data Cleaning & Feature Extraction</div>

          <div style="color:var(--accent-indigo); font-weight:700;"><i class="fas fa-filter"></i> 2. PREPROCESSING & NORMALIZATION</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • MinMaxScaler Normalization (0 to 1 Scaling)<br>
            • Sliding Window Sequence Creation (60-day Lookback Window)
          </div>

          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Passes Sequences into Neural Network</div>

          <div style="color:var(--accent-emerald); font-weight:700;"><i class="fas fa-brain"></i> 3. LSTM DEEP LEARNING MODEL</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Multi-layered LSTM Recurrent Neural Net with Dropout Layers<br>
            • Trained on Historical Patterns to Predict Future Equity Trends
          </div>

          <div style="padding-left:1.5rem; color:var(--text-muted);">↓ Model Prediction Output</div>

          <div style="color:var(--accent-amber); font-weight:700;"><i class="fas fa-chart-line"></i> 4. FLASK REST SERVICE & VISUALIZATION</div>
          <div style="padding-left:1.5rem; color:var(--text-secondary); font-size:0.82rem;">
            • Exposes Prediction Endpoint & Renders Trend Chart
          </div>
        </div>
      `
    }
  };

  document.querySelectorAll('.trigger-arch-modal').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const projId = btn.getAttribute('data-project');
      const data = architectureData[projId] || architectureData['rest-api'];

      titleEl.innerHTML = `<i class="fas fa-sitemap" style="color:var(--accent-indigo);"></i> ${data.title}`;
      descEl.textContent = data.desc;
      contentEl.innerHTML = data.content;

      overlay.classList.add('active');
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => overlay.classList.remove('active'));
  }

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.classList.remove('active');
  });
}

/* CONTACT FORM VALIDATION & TRANSMISSION */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;

    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Transmitting Message...';
    btn.disabled = true;

    setTimeout(() => {
      btn.innerHTML = '<i class="fas fa-check"></i> Message Transmitted!';
      btn.style.background = 'var(--accent-emerald)';
      btn.style.borderColor = 'var(--accent-emerald)';
      btn.style.color = '#ffffff';

      setTimeout(() => {
        form.reset();
        btn.innerHTML = originalText;
        btn.style.background = '';
        btn.style.borderColor = '';
        btn.style.color = '';
        btn.disabled = false;
      }, 3000);
    }, 1200);
  });
}

/* ACTIVE NAV LINK */
function initActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    let current = '';
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
      const sectionTop = section.offsetTop - 120;
      const sectionHeight = section.offsetHeight;
      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  });
}
