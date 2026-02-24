# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.9.1] - 2026-02-24

### Added (1.9.1)

- **IONOS Documentation Search (MCP)** — AI assistant can now search the official IONOS Cloud documentation via the GitBook MCP server (`docs.ionos.com/cloud/~gitbook/mcp`). Toggle the "Docs" button in the AI panel header to enable/disable. Results are appended to AI context so answers are grounded in official product docs.
- MCP client with session management: `initialize` → `tools/list` (auto-discovers search tool) → `tools/call` with JSON-RPC 2.0 over Streamable HTTP
- New `/mcp-docs` proxy endpoint in `serve.py` — forwards JSON-RPC requests to GitBook MCP, handles SSE-to-JSON conversion for Streamable HTTP transport
- **Feature carousel on pre-login onboarding** — 5-slide auto-rotating showcase (AI Cloud Assistant, Global Traffic Map, DNS & CDN Discovery, Flow Log Explorer, Billing & Data Transfer) with dot navigation, pause-on-hover
- **Progressive loading screen on connect** — 6-step animated checklist (authenticating, loading datacenters, building map, fetching billing, discovering DNS, ready) with progress bar and smooth fade-out
- **VDC drill-down loading** — 4-step animated checklist (servers, NICs, managed services, graph rendering) matching the connect loading style for consistency
- AI context scoping labels: `[Contract-wide]` prefix for billing/VDC inventory sections, `[VDC-name]` prefix for topology, servers, LANs, databases, security sections. System prompt instructs the AI to distinguish between contract-wide and VDC-specific data.

### Changed (1.9.1)

- VDC inventory in AI context now sourced from Cloud API `/cloudapi/v6/datacenters` instead of billing API — fixes inaccurate counts (billing included deleted VDCs, missed zero-traffic ones)
- Removed pricing labels from AI model selector dropdown and README (costs change frequently)
- AI-first README hero section with tagline and dedicated AI Cloud Assistant section with example prompts
- Onboarding subtitle updated across all 4 locales to highlight AI-powered insights
- `serve.py` CORS headers updated to expose `Mcp-Session-Id` for MCP session management

### Fixed (1.9.1)

- AI panel close animation causing layout glitch — content overflowing during width transition. Fixed by using `min-width` transition, removing `overflow: visible`, and conditionally applying `border-left` only when panel is open
- White/blue band across map when AI panel is open during navigation — Leaflet default `#ddd` background was showing through unloaded tiles; set map container background to `var(--bg-primary)`. Added `ResizeObserver` on `.main-area` for automatic `invalidateSize`. Root fix: AI panel now auto-closes before map navigation so container dimensions are stable when Leaflet calculates tile bounds
- Toolbar buttons overflowing outside the bar when AI panel is open — added `max-width: calc(100% - 40px)` constraint with flexible button shrinking; reduced padding and gap for compact layout
- AI panel auto-closes on navigation (global map, VDC switch, location view) to prevent map resize artifacts and toolbar overflow
- VDC loading overlay showing onboarding content bleed-through — changed from semi-transparent `rgba(15, 23, 42, 0.85)` to fully opaque `var(--bg-primary)` with `z-index: 200`
- MCP docs search failing silently — added SSE response parsing in proxy, dynamic tool name discovery via `tools/list`, robust JSON-RPC error handling, and diagnostic logging

## [1.9.0] - 2026-02-23

### Added (1.9.0)

- **AI Cloud Assistant** — General-purpose AI-powered infrastructure analysis using IONOS AI Model Hub (OpenAI-compatible API). Analyzes topology, security posture, billing/traffic, flow logs, and database services. Slide-out chat panel with multi-turn conversation, model selector (Llama 3.1 8B, Mistral Small 24B, Llama 3.3 70B), cost banner, and context-aware quick suggestions. Press `A` to open.
- Dynamic AI context builder (`buildAiContext`) sends topology summary, server inventory with specs, LAN layout, database services, network infrastructure, security posture metrics, billing/data transfer stats, and flow log analysis to the model
- Dynamic suggestion buttons that adapt based on loaded data: infrastructure summary, security assessment, traffic patterns, rejected flows, cost optimization, database overview
- Context-aware system prompt (`buildAiSystemPrompt`) adapts persona based on available data (topology, flow logs, billing)
- All VDC names from billing API included in AI context (covers entire contract, not just loaded VDC)
- **Flow Log Enrichment** — IP-to-resource tagging (maps IPs to servers/services via topology), well-known port labels (SSH, HTTP, HTTPS, MySQL, etc.), and threat/scan flagging (Telnet, SMB, RDP, VNC + ICMP probes on REJECT)
- NIC-to-server resolution: "Server / NIC" column shows server name alongside full NIC UUID
- "External" badge on REJECT rows for unresolved IPs
- **Right-click context menu** on flow log rows: Copy Row, Copy Source IP, Copy Dest IP, Copy NIC UUID, Copy as JSON, Filter by Source IP, Filter by Dest IP. Works in both inline and pop-out tables.
- Horizontal scroll on enriched flow log table (`min-width: 1100px`)
- Proxy POST support in `serve.py` for AI Model Hub API (`do_POST` handler forwarding request body)

### Changed (1.9.0)

- AI panel title: "Network AI Assistant" → "AI Cloud Assistant"
- AI button now visible as soon as topology loads (not only when flow logs are loaded)
- AI model costs updated to EUR pricing from official IONOS SE price list
- `escapeHtml()` rewritten from DOM-based (createElement per call) to pure string replacement — eliminates thousands of temporary DOM elements during table rendering
- System prompt includes anti-hallucination instruction: "Only reference resources explicitly present in context"
- `serve.py` CORS headers updated to allow POST method
- Locale dropdown alignment: consistent 28px height matching theme toggle, centered vertically

### Fixed (1.9.0)

- Context menu click handlers not firing: root cause was `flCtxRecord` set before `hideFlContextMenu()` which nulled it out; moved assignment after hide call
- Context menu event delegation: replaced `DOMContentLoaded` wrapper (already fired by script execution time) with direct event delegation on `#flContextMenu` using `e.stopPropagation()`
- AI guard blocking all messages when no flow logs loaded — now allows messages with topology-only data

### Security (1.9.0)

- Prompt injection defence: new `sanitizeName()` strips newlines, control characters, and limits to 100 chars on all infrastructure names before AI context embedding
- AI context overflow protection: `AI_MAX_CONTEXT_CHARS` (12,000) truncates large topologies to stay within model token limits
- AI request timeout: `AbortController` with 45-second timeout prevents hung requests
- AI rate limiting: 2-second cooldown between requests prevents spam
- HTTP 429 (rate limit) error now shows specific user-facing message
- In-flight AI requests cancelled on disconnect cleanup

## [1.8.1] - 2026-02-23

### Added (1.8.1)

- Flow Log Explorer dockable bottom-panel mode: toggle between centered overlay and bottom-docked panel to keep the map visible while browsing flow logs
- Dock toggle button in Flow Log Explorer header with distinct float/dock icons
- Top-edge resize handle in docked mode for adjustable panel height (drag to resize, persisted via localStorage)
- Dock preference persisted across sessions via localStorage
- Row click in docked mode highlights the selected row in-place and keeps the explorer open (no need to close/reopen)
- Pop-out to separate window: open the Flow Log Explorer in its own browser window (drag to a second monitor) with full filter/sort/page controls and real-time hover-to-highlight on the main map
- Pop-out window auto-syncs filters, sorting, pagination, and NIC options with the main app
- Connection status indicator in pop-out footer; graceful handling when main window is closed

### Fixed (1.8.1)

- README banner SVG: removed duplicate IONOS logo box, single centered wordmark with proper spacing

## [1.8.0] - 2026-02-20

### Added (1.8.0)

- Data Transfer integration via IONOS Billing API v3 (`/billing/{contract}/traffic` and `/billing/{contract}/utilization`)
- Global Map Data Transfer panel: floating table (top-right) showing per-region In/Out totals on overview, per-VDC breakdown on drill-down
- Server detail Data Transfer chart: 30-day daily inbound/outbound grouped bar chart (D3.js) in the detail panel
- Data Transfer Heatmap mode (`B` key): per-server transfer volume visualization as SVG halos on the topology graph
- Standalone Data Transfer Heatmap toolbar button (separated from Flow Logs dropdown)
- Heatmap legend mode toggle: Volume / Security / Transfer with dedicated gradient for Transfer mode
- Billing data auto-scales display units (MB / GB / TB) based on magnitude
- i18n translations for Data Transfer features in all 4 locales (EN, DE, ES, FR)

### Changed (1.8.0)

- Heatmap legend repositioned from bottom-right to top-right for consistency with Data Transfer panel
- Heatmap legend styling updated: backdrop blur, matching border radius and shadow as other panels
- Billing data fetch moved earlier in connect flow (starts before user info fetch) for faster panel display
- Heatmap clears automatically when navigating from VDC topology to Global Map view
- Renamed all "Billing Traffic" / "Billing Heatmap" labels to "Data Transfer" / "Data Transfer Heatmap" across all locales
- Favicon updated to IONOS-style network topology icon (inline SVG, no external file dependency)
- Sidebar header replaced with official IONOS Cloud logo (vector paths from brand assets, theme-aware via `currentColor`)
- README banner SVG (`docs/ionos-cloud-banner.svg`) updated with official IONOS Cloud logo vector paths
- Onboarding card redesigned: official IONOS Cloud logo replaces duplicate title, subtitle updated to mention flow logs and data transfer
- Onboarding step 3 text updated to reflect full feature set (topology, flow logs, data transfer, export)
- Onboarding step 1 corrected: "Token Management" → "Token Manager" across all locales
- Map reflows correctly on sidebar collapse/expand (`invalidateSize` called after transition)

### Fixed (1.8.0)

- Billing API `/traffic/` response parsing: fixed `trafficObj.vdc` array iteration (was incorrectly using `Object.entries`)
- Billing API `/utilization/` response parsing: fixed `datacenters[].meters[]` structure, `quantity.quantity` object extraction, and `meter.from` date field
- Heatmap legend not hiding when switching from VDC topology to Global Map view
- Data Transfer panel not hiding when navigating away from map view (triple-layer enforcement: `hideMapOverview`, `setViewMode`, and `updateMapBillingPanel` guard)
- Disconnect cleanup: billing state variables properly reset
- Onboarding card disappearing when navigating to Global Map pre-login (`showMapOverview` now preserves it in pre-login state)
- Onboarding logo invisible in light mode (hardcoded `fill="white"` → theme-aware `fill="currentColor"`)

## [1.7.0] - 2026-02-20

### Added (1.7.0)

- Flow Log Explorer (`W` key): drag-and-drop upload of IONOS flow log files (.log, .log.gz) with client-side gzip decompression via Pako.js
- Flow log table with sortable columns, pagination, and per-page size selector (25/50/100/200)
- Flow log filters: source/destination IP, port range, protocol dropdown, action (ACCEPT/REJECT), and NIC interface selector
- Flow log file pills: visual indicators showing loaded files with record counts and click-to-remove
- Flow log statistics bar: total records, accept/reject counts with color-coded indicators
- Flow log CSV export of filtered records
- Flow log path highlighting: click a flow record to trace source→destination path on the graph using BFS path-finding with up to 4 intermediate hops
- Flow log hover highlighting: hover a table row to temporarily highlight the matching path on the graph
- Persistent flow highlights with "click map to clear" toast and movable highlight dialog showing matched resources
- Traffic Heatmap (`X` key): visual overlay showing per-node traffic volume or security risk as color-coded SVG halos with Gaussian blur filters
- Heatmap mode toggle: switch between Volume (bytes transferred) and Security (rejected packet ratio) views
- Heatmap gradient legend with min/max labels and aggregate statistics
- Flow Logs toolbar dropdown: unified menu replacing individual toolbar buttons, with Explorer and Heatmap options showing keyboard shortcuts
- Resizable Flow Log Explorer dialog with drag handle, min-width/min-height constraints, and `resize: both` CSS

### Changed (1.7.0)

- Toolbar: Flow Log Explorer and Traffic Heatmap consolidated into a single dropdown menu (matches export dropdown pattern)
- VDC sidebar dropdown font size normalized to 12px to match other sidebar elements
- Escape key handling extended: closes flow log dropdown, heatmap overlay, and flow log explorer in priority order
- Map click handler extended: clicking the map background now also clears active heatmap overlays

### Improved (1.7.0)

- Tick callback performance: pre-cached VDC node references and replaced 4× `d3.min/max` calls with single-pass bounds calculation
- Heatmap halo position updates: uses pre-built `_nodeMap` for O(1) lookups instead of `Array.find()` in hot path
- Flow log parsing: `Array.push(...records)` instead of `Array.concat()` to avoid full-array copy on each file load
- Flow log table rendering: array-based HTML assembly with `.join()` instead of string concatenation
- Flow log statistics: single-pass accept/reject counting instead of two separate `.filter()` scans
- Heatmap data aggregation: memoized `aggregateFlowData()` with automatic cache invalidation on data changes
- Flow path resolution: persistent IP→nodeId, NIC→nodeId, and BFS adjacency lookup maps built once in `renderGraph()`, reducing `resolveFlowPath()` from O(n) node scan per call to O(1) map lookups
- Event listener deduplication: `_flDropBound` guard prevents accumulating duplicate drag/drop handlers on repeated dialog opens
- Error handling: `parseFlowLogFile` wraps `file.arrayBuffer()` in try/catch with descriptive error propagation

## [1.6.0] - 2026-02-16

### Added (1.6.0)

- Internationalization (i18n) with 4 locales: English, German, Spanish, French (164 translation keys)
- Language switcher dropdown in sidebar header with flag icons and active indicator
- Dark / Light theme toggle with system preference detection and localStorage persistence
- Light theme CSS variables and Leaflet map tile swapping (Carto `dark_all` ↔ `light_all`)
- VDC Favorites: pin/unpin VDCs with star button, persisted in localStorage, pinned VDCs sorted to top of dropdown with separator
- Security Posture overlay (`S` key): 5 metrics (Firewall, Flow Logs, Security Groups, Private LANs, IPv6) with color-coded progress bars and click-to-highlight
- NAT Gateway upsell suggestion in Security Posture — warns when private LANs lack a NAT Gateway
- Disconnect button: Connect button transforms to Disconnect after login, cleanly resets all state and restores the onboarding welcome screen
- Connection IPs for managed services (PostgreSQL, MongoDB, MySQL, MariaDB, NFS) displayed on nodes in IP view and detail panel
- Security rules table in VM detail panel with columns: Direction (color-coded), Protocol, Ports, Source, Target
- Light theme overrides for map tiles, cluster bubbles, toast shadows, and IP view labels

### Changed (1.6.0)

- Sidebar header redesigned: compact layout with IONOS Cloud title, subtitle, and theme/locale controls grouped in one row
- Highlights toolbar icon changed from shield to eye icon (differentiated from Security Posture shield)
- Fit-to-view and Reset-view toolbar buttons merged into single "Reset & fit view" button (`F` / `R` keys)
- Reset view now fully resets IP view, Compute view, highlights, and all overlays
- Security group IDs stored as UUIDs instead of names (fixes lookup against `_securityGroups` map)
- Security group API depth increased from 2 to 3 for full rule property access
- Security group rules display upgraded from sparse one-liners to detailed table with protocol, ports, source/target, ICMP support
- IP view labels repositioned closer to nodes when active (since name/spec labels are hidden)
- IP view labels styled with stroke outline for contrast against map background
- Keyboard shortcut `S` opens Security Posture; `F` now calls resetView instead of standalone zoomFit

### Fixed (1.6.0)

- Light mode not changing the map tiles (Leaflet used hardcoded dark tiles)
- Security rules section always empty in VM detail panel (name vs UUID mismatch in security group lookup)
- Security rules showing only "⬇ ANY" with no useful details (API depth too shallow)
- Duplicate IPs appearing at edge of map in IP view (SVG tspan `x=0` snapping to absolute origin)
- Link labels overlapping node IP sublabels in IP view (now hidden via CSS since they duplicate node labels)
- Reset & Fit not clearing IP view, Compute view, or highlight checkboxes
- Onboarding welcome screen not reappearing after disconnect (showMapOverview was hiding it)
- Managed service nodes (DBaaS, NFS) missing private IPs in IP view and resource table

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
