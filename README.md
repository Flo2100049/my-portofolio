# Cloud-Native Personal Portfolio

Αυτό το project είναι μια **Cloud-Native, containerized πλατφόρμα** που φιλοξενεί το προσωπικό μου portfolio. Δεν πρόκειται για μια απλή στατική σελίδα, αλλά για ένα κατανεμημένο σύστημα (distributed system) που χρησιμοποιεί microservices, event-driven αρχιτεκτονική και GitOps πρακτικές.



## Architecture Overview
Η πλατφόρμα έχει σχεδιαστεί για scalability και fault tolerance:
- **Frontend:** HTML/CSS/JS served μέσω NGINX.
- **Backend:** Python (Flask API) που διαχειρίζεται τα requests και επικοινωνεί με τη βάση.
- **Async Processing:** Χρήση **RabbitMQ** ως message broker για να διασφαλιστεί ότι τα notifications (email/WhatsApp) εκτελούνται asynchronous, χωρίς να καθυστερούν το API.
- **Database:** MongoDB για την αποθήκευση των μηνυμάτων επικοινωνίας.

## Tech Stack
- **Languages:** Python (Flask), JavaScript
- **Infrastructure:** Kubernetes (DOKS), NGINX Ingress Controller
- **Message Broker:** RabbitMQ
- **DevOps:**
  - **CI/CD:** GitHub Actions (Automated image builds & manifest patching)
  - **GitOps:** ArgoCD (Continuous delivery & cluster synchronization)
  - **Security:** Cert-manager (Let's Encrypt SSL/TLS)

## Engineering Highlights
* **Event-Driven Design:** Υλοποίηση ενός publisher/consumer pattern. Το backend "σπρώχνει" μηνύματα στο RabbitMQ και ένας dedicated `notification-worker` τα επεξεργάζεται, επιτρέποντας στο σύστημα να αντέχει spikes στην κίνηση.
* **GitOps Workflow:** Το cluster είναι πάντα συγχρονισμένο με το repo. Κάθε αλλαγή στον κώδικα triggerάρει build, ενημερώνει τα Kubernetes manifests αυτόματα μέσω του CI pipeline και το ArgoCD αναλαμβάνει το deployment.
* **Reliability & Security:** Υλοποίηση HTTPS μέσω cert-manager και σωστό configuration του Ingress controller για ασφαλή επικοινωνία.

## Challenges Faced & Solved
* **Memory Management:** Αντιμετώπιση `OOMKilled` errors περιορίζοντας τα resource limits (requests/limits) στα containers για να αποφευχθεί η υπερκατανάλωση μνήμης σε περιορισμένο hardware (1GB RAM).
* **Networking:** Debugging του ingress controller για την επίλυση του PROXY protocol και τη σωστή δρομολόγηση του traffic στο domain μου (`floriankamaj.dev`).
* **Asynchronous Logic:** Χειρισμός του 24-hour window policy του WhatsApp API μέσω σωστού worker implementation.

## Live Demo
Δείτε το project live εδώ: [floriankamaj.dev](https://floriankamaj.dev)

---
*Developed by Florian Kamaj | Dedicated to building robust software systems.*