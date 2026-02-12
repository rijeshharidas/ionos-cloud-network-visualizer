# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-02-12

### Added (1.5.0)

- Resource Table View (`T` key): full-screen overlay with sortable, searchable table of all resources
- Type filter pills in table view — click to toggle resource types, each with count badge
- Column sorting (Name, Type, State) with visual sort indicators
- Text search across name, type, state, details, and IPs with debounced filtering
- Row click in table closes overlay and zooms to that node on the graph
- CSV export from table view (filtered rows)
- Export dropdown menu: consolidated PNG/SVG/JSON buttons into a single dropdown with 6 formats
- CSV export (all resources, unfiltered) via export dropdown
- XLSX export: multi-sheet workbook with Resources, Connections, and Summary sheets
- PDF export: landscape report with topology diagram on page 1 and styled resource inventory table on page 2+
- SheetJS, jsPDF, and jsPDF-AutoTable libraries loaded via CDN

### Changed (1.5.0)

- Toolbar: 3 individual export buttons replaced by a single export dropdown (reduces toolbar clutter)
- Export dropdown opens upward from toolbar with section labels (Diagram / Data / Report)
- Click-outside and Escape key close the export dropdown

## [1.4.0] - 2026-02-11

### Added (1.4.0)

- Docker support: Dockerfile and .dockerignore for containerized deployment
- `--host` flag on serve.py to allow binding to custom addresses (needed for Docker)

### Changed (1.4.0)

- Compute View: condensed to 2-line labels (type + CPU on line 1, cores/RAM on line 2)
- Compute View: GPU classification now based on VM type instead of CPU family
- IP View: new text elements with absolute positioning for reliable label layout
- IP View: all IP labels consistently styled in blue; non-IP content fully dimmed
- Both views use appended text elements instead of modifying existing ones (fixes label overlap)

## [1.3.0] - 2026-02-10

### Added (1.3.0)

- Global map shows all IONOS data center locations as faded markers (pre-login and post-login)
- Dynamic location discovery via `/cloudapi/v6/locations` API after authentication
- Cloud DNS integration: sidebar panel with zone list, record counts, and forward DNS lookup
- Reverse DNS enrichment on IP View labels (IP addresses show hostnames in parentheses)
- CDN badge on DNS zones that have CDN distributions configured; muted "No CDN" indicator on zones without CDN
- Compute View toggle (`C`) showing VM type, cores, RAM, and CPU family on server/cube nodes, color-coded by type (Enterprise/vCPU/Cube/GPU)
- DNS Names and Reverse DNS rows in node detail panel for resources with public IPs
- Public IP block sidebar panel showing IPv4 and IPv6 allocations
- GitHub Sponsors heart icon in sidebar footer
- SVG and JSON export options alongside existing PNG export

### Changed (1.3.0)

- Global Map now fits all DC locations (active + available) in view bounds
- IP View icon changed from globe to bordered "IP" text for clarity
- Improved zoom behavior for small VDCs (adaptive padding, minimum bounding box)
- Map background opacity increased to 0.85 for better visibility
- Highlights overlay auto-closes on navigation to Global Map or different VDC

### Fixed (1.3.0)

- Node dimming persisting after closing detail panel (clearHighlight on close)
- NFS and VPN status indicator dots not showing (metadata.status fallback)
- CDN badge matching for subdomains (e.g., `www.example.com` matching `example.com` zone)
- IP labels not resetting when toggling IP View off
- README tagline incorrectly mentioning firewall rules

## [1.2.0] - 2026-02-07

### Added

- Animated traffic flow visualization on links between active/running resources with glowing effect
- Security highlight rings (SVG circles/polygons) around nodes with active firewall, flow logs, security groups, IPv6, IP failover, or cross connects
- Connected-component graph clustering to automatically separate unrelated network groups into distinct visual regions
- Hierarchical force layout: Cross Connect → Internet → LANs → VMs and managed services
- Per-LAN Internet nodes to reduce visual clutter (each public LAN gets its own Internet icon)
- Sidebar re-expand button on canvas when sidebar is collapsed
- Canvas-based floating search bar (moved from sidebar to graph overlay)
- IONOS branded logo in sidebar header
- Infrastructure-aware traffic flow: Internet, LAN, and PCC nodes treated as always-active for animation

### Changed

- LAN icon redesigned from hub-spoke pattern to network switch icon to avoid confusion with Kubernetes
- NAT Gateway icon redesigned from box-with-arrows to router/gateway symbol (circle with directional arrows) for clear distinction from servers
- VDC dropdown now shows location in brackets: "VDC Name (Frankfurt 2)"
- Location labels properly handle 3-part location strings (e.g., `de/fra/2` → Frankfurt 2)
- Security highlights upgraded from CSS glow filters to SVG ring elements for better visibility
- Force simulation uses cluster-aware X positioning: child nodes pulled toward their parent LAN column
- Increased LAN charge and collision radius for better spacing
- Search icon properly sized inside input field (was rendering oversized)
- NIC labels simplified to show IP address only (removed NIC name prefix)

### Removed

- Link types legend from canvas/toolbar (removed due to layout conflicts)

### Fixed

- Sidebar collapse button no longer lost when sidebar is hidden (expand button persists on canvas)
- Traffic flow animation now works for cross connect and VPN gateway connections
- Highlight rings render on top of nodes (SVG paint order fixed)
- Location label rendering for multi-segment locations in VDC dropdown

## [1.1.0] - 2026-02-06

### Added (1.1.0)

- Node search bar with type-ahead filtering for quick resource lookup
- Welcome onboarding experience with guided setup steps
- Color-coded link types (NIC, cross connect, managed service, gateway)
- Node status indicators showing resource state (AVAILABLE, BUSY, INACTIVE)
- Collapsible sidebar for expanded graph workspace
- Keyboard shortcuts (Escape, Ctrl+F, +/-, F, L, ?)
- Staged loading progress bar with resource-level status
- Interactive stat cards with click-to-filter behavior
- Quick action toolbar buttons (Reset, Select All, Deselect All)
- `.gitignore` for clean repository management
- `CHANGELOG.md` for version tracking
- GitHub Actions CI workflow for automated validation

### Changed (1.1.0)

- Renamed project from "VDC Visualizer" to "IONOS Cloud Network Visualizer"
- Renamed `vdc-visualizer.html` to `ionos-cloud-network-visualizer.html`
- Updated README with badges and improved documentation
- Enhanced toolbar with additional quick action buttons

## [1.0.0] - 2026-01-15

### Added (1.0.0)

- Interactive force-directed graph visualization of IONOS Cloud VDC resources
- Support for 16 resource types: servers, LANs, databases, VPN, NFS, K8s, load balancers, cross connects
- NIC-to-LAN connection mapping with IP address labels
- Security highlights for firewall, flow logs, security groups, IPv6, IP failover, cross connects
- Detailed inspection panel with resource properties
- User account information display (email, contract number)
- PNG export with high-resolution rendering
- Country flags and datacenter location labels
- JWT token decode fallback for user information
- Lightweight Python proxy server with CORS support
- Port auto-fallback when default port is busy
- IONOS Cloud brand colors and Inter typography
- Apache 2.0 open source license
- README, CONTRIBUTING, and LICENSE documentation
