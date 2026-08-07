/* 
   INTERACTIVE CYBER TERMINAL ("NEXUS-901")
*/

class CyberTerminal {
  constructor() {
    this.outputContainer = document.getElementById('term-output');
    this.inputField = document.getElementById('term-input');
    this.history = [];
    this.historyIdx = -1;

    if (!this.inputField) return;

    this.init();
  }

  init() {
    this.inputField.addEventListener('keydown', (e) => {
      if (window.cyberAudio) window.cyberAudio.playKeySFX();

      if (e.key === 'Enter') {
        const cmd = this.inputField.value.trim();
        if (cmd) {
          this.executeCommand(cmd);
          this.history.push(cmd);
          this.historyIdx = this.history.length;
          this.inputField.value = '';
        }
      } else if (e.key === 'ArrowUp') {
        if (this.historyIdx > 0) {
          this.historyIdx--;
          this.inputField.value = this.history[this.historyIdx];
        }
      } else if (e.key === 'ArrowDown') {
        if (this.historyIdx < this.history.length - 1) {
          this.historyIdx++;
          this.inputField.value = this.history[this.historyIdx];
        } else {
          this.historyIdx = this.history.length;
          this.inputField.value = '';
        }
      }
    });

    // Quick Command Buttons
    document.querySelectorAll('.quick-cmd-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const cmd = btn.getAttribute('data-cmd');
        if (cmd) {
          if (window.cyberAudio) window.cyberAudio.playClickSFX();
          this.executeCommand(cmd);
        }
      });
    });
  }

  printLine(text, type = 'normal') {
    const div = document.createElement('div');
    div.className = 'term-line';
    
    if (type === 'prompt') {
      div.innerHTML = `<span class="term-prompt">user@ashok-nexus:~$</span> ${text}`;
    } else if (type === 'accent') {
      div.innerHTML = `<span class="accent">${text}</span>`;
    } else if (type === 'success') {
      div.innerHTML = `<span class="success">${text}</span>`;
    } else if (type === 'warning') {
      div.innerHTML = `<span class="warning">${text}</span>`;
    } else {
      div.innerHTML = text;
    }

    this.outputContainer.appendChild(div);
    this.outputContainer.parentElement.scrollTop = this.outputContainer.parentElement.scrollHeight;
  }

  executeCommand(cmdRaw) {
    const cmd = cmdRaw.toLowerCase().trim();
    this.printLine(cmdRaw, 'prompt');

    switch (cmd) {
      case 'help':
        this.printLine(`
AVAILABLE COMMANDS:
------------------------------------------------------------------
<span class="accent">bio</span>       : View professional summary & background
<span class="accent">skills</span>    : Display technical stack breakdown & proficiency
<span class="accent">projects</span>  : List backend REST API, Java, & ML projects
<span class="accent">edu</span>       : Show academic background & CGPA
<span class="accent">certs</span>     : Display certifications & achievements
<span class="accent">contact</span>   : View phone, email, and social profiles
<span class="accent">matrix</span>    : Toggle background canvas (matrix / nodes / hybrid)
<span class="accent">hack</span>      : Launch cyber matrix system overload sequence
<span class="accent">clear</span>     : Clear terminal buffer
------------------------------------------------------------------
`, 'normal');
        break;

      case 'bio':
      case 'about':
        this.printLine(`
[SYSTEM INFO]: ASHOK GOWDA S P
------------------------------------------------------------------
Software Engineer specializing in Java, Spring Boot, RESTful APIs,
Object-Oriented Design, and Database Architecture.
Passionate about building high-performance scalable backends.
Current Location: Bengaluru, India
Degree: B.E. Information Science and Engineering (2023 - 2027)
------------------------------------------------------------------
`, 'success');
        break;

      case 'skills':
        this.printLine(`
[TECHNICAL MATRIX]:
- Languages    : Java, SQL, Python, JavaScript
- Frameworks   : Spring Boot, Spring Data JPA, Hibernate
- Web Tech     : RESTful APIs, HTML5, CSS3, JavaScript
- Databases    : MySQL, MongoDB
- Tools & IDEs : Git, GitHub, IntelliJ IDEA, VS Code, Maven, Postman
`, 'accent');
        break;

      case 'projects':
        this.printLine(`
[FEATURED PROJECTS]:
1. <span class="accent">Employee Management System REST API</span>
   Stack: Java | Spring Boot | Hibernate | MySQL | Postman
   Architecture: Layered Controller-Service-Repository

2. <span class="accent">Employee Management System (Console)</span>
   Stack: Core Java | JDBC | MySQL | OOP Design

3. <span class="accent">Stock Market Price Prediction</span>
   Stack: Python | Pandas | Flask | LSTM Deep Learning
`, 'normal');
        break;

      case 'edu':
        this.printLine(`
[ACADEMIC TIMELINE]:
- <span class="accent">Don Bosco Institute of Technology, Bengaluru</span>
  B.E. Information Science & Engineering | 2023 - 2027 | CGPA: 9.01
- <span class="accent">Hoysala PU College, Nelamangala</span>
  Class XII | 2023 | Score: 89%
- <span class="accent">Gurukula Vidya Mandira, Kudur</span>
  Class X | 2021 | Score: 92%
`, 'normal');
        break;

      case 'certs':
      case 'achievements':
        this.printLine(`
[HONORS & CERTIFICATIONS]:
★ Gold Badge in Problem Solving (HackerRank)
★ DSA in Java (Infosys Springboard)
★ Prompt Engineering & Programming with OpenAI (Columbia University)
`, 'warning');
        break;

      case 'contact':
        this.printLine(`
[COMMUNICATIONS CHANNEL]:
Email    : imashoksp@gmail.com
Phone    : +91 8618977119
Location : Bengaluru, Karnataka, India
GitHub   : github.com/imashoksp (EmployeeManagementAPI)
LinkedIn : linkedin.com/in/ashok-gowda-s-p
`, 'success');
        break;

      case 'matrix':
        if (window.matrixEngine) {
          const modes = ['matrix', 'nodes', 'hybrid'];
          const nextMode = modes[(modes.indexOf(window.matrixEngine.mode) + 1) % modes.length];
          window.matrixEngine.switchMode(nextMode);
          this.printLine(`[CANVAS ENGINE]: Switched mode to <span class="accent">${nextMode.toUpperCase()}</span>`, 'success');
        }
        break;

      case 'hack':
        this.runHackSequence();
        break;

      case 'clear':
        this.outputContainer.innerHTML = '';
        break;

      default:
        this.printLine(`Command not recognized: '${cmdRaw}'. Type '<span class="accent">help</span>' for menu.`, 'warning');
        break;
    }

    if (window.cyberAudio && cmd !== 'hack') window.cyberAudio.playSuccessSFX();
  }

  runHackSequence() {
    this.printLine('[INITIATING SYSTEM OVERLOAD SEQUENCE...]', 'warning');
    let step = 0;
    const lines = [
      '01000001 01010011 01001000 01001111 01001011',
      'BYPASSING FIREWALL... [SUCCESS]',
      'DECRYPTING SPRING BOOT REST ENDPOINTS...',
      'CONNECTING TO MYSQL CLUSTER [PORT 3306]...',
      'INITIALIZING NEURAL NETWORK LSTM WEIGHTS...',
      '<span class="success">>>> ACCESS GRANTED: WELCOME TO ASHOK GOWDA\'S SYSTEM MATRIX <<<</span>'
    ];

    const timer = setInterval(() => {
      if (step < lines.length) {
        this.printLine(lines[step], 'accent');
        if (window.cyberAudio) window.cyberAudio.playKeySFX();
        step++;
      } else {
        clearInterval(timer);
        if (window.cyberAudio) window.cyberAudio.playSuccessSFX();
      }
    }, 400);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.cyberTerminal = new CyberTerminal();
});
