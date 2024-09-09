## Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/sawadogosalif/openwebui.git
   cd data-scientist-workbench
   ```

2. **Configure Environment Variables**
   Update a `default.env` file in the root directory with the following variables as you want.

3. **Build and Run Services**
   ```bash
   docker-compose --env-file default.env up -d
   ```