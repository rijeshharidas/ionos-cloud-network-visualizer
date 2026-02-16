<p align="center">
  <img src="docs/ionos-cloud-banner.svg" alt="IONOS Cloud Network Visualizer" width="800">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License: Apache 2.0"></a>
  <img src="https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white" alt="Python 3.6+">
  <img src="https://img.shields.io/badge/D3.js-v7-F9A03C?logo=d3dotjs&logoColor=white" alt="D3.js v7">
  <img src="https://img.shields.io/badge/Leaflet-1.9.4-199900?logo=leaflet&logoColor=white" alt="Leaflet 1.9.4">
  <img src="https://img.shields.io/badge/Dependencies-None-brightgreen" alt="No Dependencies">
  <img src="https://img.shields.io/badge/IONOS%20Cloud-Visualizer-003D8F" alt="IONOS Cloud">
</p>

<p align="center">
  A browser-based interactive network topology visualizer for IONOS Cloud infrastructure.<br>
  See your entire cloud at a glance — from a global map of regions down to individual servers, LANs, and managed services.
</p>

---

<p align="center">
  <a href="#key-capabilities">Key Capabilities</a> &nbsp;·&nbsp;
  <a href="#quick-start">Quick Start</a> &nbsp;·&nbsp;
  <a href="#view-modes">View Modes</a> &nbsp;·&nbsp;
  <a href="#supported-resource-types">Resources</a> &nbsp;·&nbsp;
  <a href="#keyboard-shortcuts">Shortcuts</a> &nbsp;·&nbsp;
  <a href="#architecture">Architecture</a> &nbsp;·&nbsp;
  <a href="#security">Security</a> &nbsp;·&nbsp;
  <a href="#contributing">Contributing</a>
</p>

---

### Global Map & VDC Drill-Down

[![Global Map and VDC topology drill-down](docs/visualizer.gif)](docs/visualizer.gif)

### Cross-Connect Visualization (Regional View)

[![Cross-connect visualization in regional mode](docs/cross-connect.gif)](docs/cross-connect.gif)

## Key Capabilities

🗺️ **Global Map View** — An interactive geographic map displays all IONOS data center locations worldwide on first load, color-coded by cloud type (Public, Private, or both) with hover tooltips. After connecting, your active regions appear as cluster bubbles with country flags and VDC counts while available locations remain visible as faded markers. Click a region to drill down, then click a VDC to visualize its topology.

🔗 **Managed Service Visibility** — Databases (PostgreSQL, MongoDB, MySQL, MariaDB), VPN Gateways, NFS shares, Load Balancers, Kubernetes clusters, and Kafka clusters are all rendered on the topology graph, connected to the LANs they belong to. No more jumping between DCD panels.

🌐 **Regional Cross-Connect View** — Load all VDCs within a region onto a single canvas to see Private Cross Connect links between data centers. VDCs in the same metro are treated as one region since they can be interconnected.

📡 **IP & DNS View** — Toggle IP address labels across the entire topology, enriched with reverse DNS hostnames and forward DNS record names. Public IP block allocations (IPv4 and IPv6) and DNS zones are shown in dedicated sidebar panels. Zones with CDN distributions are flagged with a CDN badge; zones without CDN show a muted "No CDN" indicator.

🖥️ **Compute View** — Toggle compute details across all server and cube nodes showing VM type, CPU cores, RAM, and CPU family. Color-coded by VM type: cyan for dedicated-core (Enterprise), purple for vCPU, orange for Cube, and rose for GPU instances. Press `C` to toggle.

🛡️ **Highlights** — Filter by Firewall Active, Flow Logs, Security Groups, IPv6 Enabled, IP Failover, and Cross Connect. Matching nodes glow with highlight rings while everything else fades — compliance audits made visual.

📊 **Live Metrics** — Select a server to see 1-hour network throughput and packet count time-series charts directly in the detail panel.

🔍 **Canvas Search** — Type-ahead search across all resources with instant highlighting on the canvas. Focus with `Ctrl+F`.

🏢 **Reseller / Multi-Contract Support** — Accounts with multiple contracts (reseller masters) see a contract dropdown after login. Selecting a contract switches the entire view to that contract's resources. The selected contract is passed via the standard `X-Contract-Number` header on every API call.

📋 **Resource Table View** — Press `T` to open a full-screen searchable, sortable table of all resources. Type filter pills let you isolate specific resource types, column headers sort by name/type/state, and a text search filters across all columns. Click any row to zoom to that node on the graph. Export the filtered view as CSV directly from the table.

🛡️ **Security Posture** — Press `S` for a one-glance security summary of your VDC: Firewall Active, Flow Logs, Security Groups, Private LANs, and IPv6 coverage — each with a color-coded progress bar. Click any metric to highlight matching nodes on the graph.

🌗 **Dark & Light Theme** — Toggle between dark and light mode with automatic system-preference detection. The Leaflet map tiles swap between Carto `dark_all` and `light_all` automatically. Your preference is persisted in `localStorage`.

🌐 **Internationalization (i18n)** — Full UI translated into English, German, Spanish, and French (164 keys). Switch languages from the flag dropdown in the sidebar header. Locale is persisted in `localStorage`.

⭐ **VDC Favorites** — Pin frequently used VDCs with the star button next to the dropdown. Pinned VDCs sort to the top with a separator. Favorites persist in `localStorage` across sessions.

📤 **Export** — A unified export dropdown consolidates all formats in one place: PNG and SVG for diagrams, JSON/CSV/XLSX for data, and PDF for shareable reports. The XLSX workbook includes three sheets (Resources, Connections, Summary). The PDF report renders the topology diagram on page one with a styled resource inventory table on subsequent pages.

## Quick Start

```bash
git clone https://github.com/rijeshharidas/ionos-cloud-network-visualizer.git
cd ionos-cloud-network-visualizer
python3 serve.py
```

The server automatically opens your browser at `http://localhost:8080` (with automatic fallback to the next available port if 8080 is in use).

**No npm, no build step, no pip install required** — just Python and a browser.

1. Enter your IONOS Cloud API token
2. The Global Map loads automatically — explore your regions
3. Click into any VDC to visualize its full network topology

### Docker

```bash
docker build -t ionos-cloud-visualizer .
docker run -p 8080:8080 ionos-cloud-visualizer
```

Then open `http://localhost:8080` in your browser. No Python installation needed — just Docker.

<details>
<summary><strong>Installing Python</strong> (click to expand — skip if you already have Python 3.6+)</summary>

### macOS

Python 3 comes pre-installed on recent macOS versions. Open **Terminal** (search "Terminal" in Spotlight) and check:

```bash
python3 --version
```

If the command is not found, install Python using one of these methods:

**Option A — Official installer (recommended for non-developers):**
Download from <https://www.python.org/downloads/> and run the `.pkg` installer.

**Option B — Homebrew:**

```bash
brew install python
```

### Windows

**Option A — Official installer (recommended):**

1. Go to <https://www.python.org/downloads/>
2. Click **"Download Python 3.x.x"**
3. Run the installer — **check "Add python.exe to PATH"** at the bottom of the first screen
4. Click "Install Now"
5. Open **Command Prompt** or **PowerShell** and verify:

```cmd
python --version
```

> **Note:** On Windows, use `python` instead of `python3`:
>
> ```cmd
> python serve.py
> ```

**Option B — Microsoft Store:**
Search "Python" in the Microsoft Store and install the latest version.

### Linux (Ubuntu / Debian)

Python 3 is usually pre-installed. Check with:

```bash
python3 --version
```

If missing:

```bash
sudo apt update && sudo apt install python3
```

### Verifying Your Installation

After installation, confirm Python is available:

```bash
python3 --version   # macOS / Linux
python --version    # Windows
```

You should see `Python 3.x.x`. Any version from 3.6 onward works.

</details>

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Python 3.6+** | Standard library only — no pip dependencies needed (not required if using Docker) |
| **Modern browser** | Chrome, Firefox, Safari, or Edge |
| **IONOS Cloud API Token** | Generate at [dcd.ionos.com](https://dcd.ionos.com) under **Management > Token Management** |
| **Docker** *(optional)* | Required only if running via `docker build` / `docker run` instead of Python directly |

## View Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| 🗺️ **Global Map** | Interactive Leaflet.js map showing all IONOS DC locations with cloud type tooltips (Public / Private / Both). Active regions display as cluster bubbles with VDC counts; available locations appear as faded markers. Press `G` to return. | Navigate multi-region infrastructure |
| 🖥️ **Single VDC** | Full force-directed topology graph for one data center: servers, LANs, NICs, managed services, gateways, and load balancers. | Inspect a specific data center |
| 📍 **By Location** | All VDCs in a metro region on one canvas with Private Cross Connect links visible. | See cross-VDC connections |

## Supported Resource Types

Each resource type has a distinctive custom SVG icon for instant visual identification:

| Category | Resources |
|----------|-----------|
| **Compute** | Servers, Cube Servers, Kubernetes Node Pools |
| **Networking** | LANs, NICs, NAT Gateways, Private Cross Connects |
| **Databases** | PostgreSQL, MongoDB, MySQL, MariaDB |
| **Storage** | Network File System (NFS) |
| **Security** | VPN Gateways (WireGuard, IPSec) |
| **Load Balancing** | Application Load Balancers, Network Load Balancers |
| **Streaming** | Kafka Clusters |
| **DNS** | Public Zones, Reverse DNS Records |
| **CDN** | CDN Distributions (indicated on DNS zones) |

## Architecture

Two files, zero build process:

| File | Role |
|------|------|
| **`ionos-cloud-network-visualizer.html`** | Self-contained frontend — D3.js v7 for topology, Leaflet.js v1.9.4 for maps, all CSS/JS inline |
| **`serve.py`** | Lightweight localhost CORS proxy (Python stdlib only) bridging browser requests to IONOS Cloud APIs |

```text
Browser (localhost:8080)  →  Proxy (serve.py)  →  IONOS Cloud API (*.ionos.com)
```

Your API token never leaves your machine.

## Supported IONOS Cloud Services

| Service | API Endpoint | Scope |
|---------|--------------|-------|
| Virtual Servers | `/cloudapi/v6` | Per Data Center |
| Networks (LANs) | `/cloudapi/v6` | Per Data Center |
| Network Interfaces | `/cloudapi/v6` | Per Data Center |
| PostgreSQL | `/databases/postgresql` | Centralized |
| MongoDB | `/databases/mongodb` | Centralized |
| MySQL | `/databases/mysql` | Centralized |
| MariaDB | `mariadb.{location}.ionos.com` | Regional |
| VPN Gateway | `vpn.{location}.ionos.com` | Regional |
| Network File System | `nfs.{location}.ionos.com` | Regional |
| Kubernetes | `/cloudapi/v6` | Centralized |
| NAT Gateway | `/cloudapi/v6` | Per Data Center |
| Load Balancers | `/cloudapi/v6` | Per Data Center |
| Cross Connects | `/cloudapi/v6` | Centralized |
| Kafka | `kafka.{location}.ionos.com` | Regional |
| Cloud DNS | `dns.de-fra.ionos.com` | Centralized |
| CDN | `cdn.de-fra.ionos.com` | Centralized |
| Locations | `/cloudapi/v6/locations` | Centralized |
| User Management | `/cloudapi/v6/um` | Centralized |

## Configuration

```bash
python3 serve.py [options]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--port PORT` | `8080` | Server port (auto-increments if unavailable) |
| `--no-browser` | `false` | Don't auto-open the browser |

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `?` or `/` | Show keyboard shortcuts help |
| `Escape` | Close panels and overlays |
| `Ctrl/Cmd+F` | Focus search bar |
| `+` / `-` | Zoom in / out |
| `F` / `R` | Reset & fit to view |
| `L` | Toggle labels |
| `I` | Toggle IP view |
| `C` | Toggle compute view |
| `H` | Toggle highlights overlay |
| `S` | Security posture overlay |
| `M` | Toggle map background |
| `T` | Resource table view |
| `G` | Global map view |

## Security

| Measure | Detail |
|---------|--------|
| **Token Isolation** | Your API token never leaves your local machine. The proxy validates all requests target `*.ionos.com` only. |
| **In-Memory Storage** | Tokens live exclusively in browser memory — cleared when you close the tab. No cookies, no disk persistence. |
| **Localhost Binding** | The proxy binds to `127.0.0.1` only, preventing remote access. |
| **XSS Protection** | All user-controlled content is escaped before rendering in the DOM. |

## Contributing

We welcome contributions! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting issues, proposing features, and making pull requests.

## License

IONOS Cloud Network Visualizer is licensed under the [Apache License 2.0](LICENSE).

## Links

| | |
|---|---|
| **IONOS Cloud Platform** | <https://cloud.ionos.com> |
| **API Documentation** | <https://api.ionos.com/docs/cloud/v6/> |
| **GitHub Issues** | <https://github.com/rijeshharidas/ionos-cloud-network-visualizer/issues> |
| **IONOS Cloud Status** | <https://status.ionos.com> |

---

<p align="center"><strong>IONOS Cloud</strong> — Enterprise cloud infrastructure made simple.</p>
