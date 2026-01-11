Transform a product briefing into comprehensive product management artifacts in `docs/product/`. This command gathers required information through structured questioning and generates rich, market-viable product documentation.

## Process

### 1. Accept & Analyze Product Briefing

Parse the command input for any provided product briefing:
- Extract product name/description if provided
- Identify what information is already available
- Determine what critical information is missing
- Note the level of detail provided (minimal, moderate, comprehensive)

If no briefing is provided or input is minimal (< 50 words), prepare for comprehensive questioning.

**Extract Research Keywords**:
- Identify domain/industry from briefing (e.g., "healthcare", "finance", "collaboration")
- Extract technology hints (e.g., "mobile app", "web platform", "API")
- Note use case type (e.g., "task management", "document editing", "analytics")

### 2. Conduct Domain-Expert Research (NEW)

**CRITICAL**: Before asking user questions, conduct comprehensive research across 4 knowledge sources to gather intelligence. This research will inform smarter questioning and pre-populate artifacts with validated, research-backed content.

**Research Phase Workflow**:

#### 2.1 Technology Documentation Research (Context7)

Use Context7 to query relevant technology documentation and best practices:

1. **Identify Technology Candidates** from briefing
   - If briefing mentions specific technologies, query those
   - If domain hints at tech (e.g., "mobile" → React Native/Flutter, "web" → React/Vue)
   - Query multiple options for comparison

2. **Query Context7 for Documentation**:
   ```
   # Example workflow
   resolve-library-id(
     query="[Technology description from briefing]",
     libraryName="[framework/library name]"
   ) → libraryId

   query-docs(
     libraryId="[returned library ID]",
     query="best practices for [specific use case from briefing]"
   ) → Documentation findings
   ```

3. **Research Areas**:
   - Framework/library best practices
   - Architecture patterns for the technology
   - State management approaches
   - Performance considerations
   - Security best practices
   - Testing strategies

4. **Compile Findings**:
   - List researched technologies with Context7 references
   - Note recommended patterns and anti-patterns
   - Identify library versions and compatibility
   - Document best practices found

**Limit**: Query 3-5 relevant technologies maximum (don't over-research)

#### 2.2 Architecture Pattern Research (WebSearch + WebFetch)

Use WebSearch and WebFetch to research architecture patterns for the product domain:

1. **Search for Architecture Patterns**:
   ```
   WebSearch("[domain/use case] architecture patterns 2026")
   WebSearch("[domain] scalability best practices 2026")
   WebSearch("microservices vs monolith [domain] 2026")
   ```

2. **Fetch Implementation Guides**:
   - If search finds relevant whitepapers, use WebFetch to extract details
   - Look for case studies from similar products
   - Find architecture decision frameworks

3. **Research Areas**:
   - Common architecture patterns for domain (monolith, microservices, serverless)
   - Scalability considerations and bottlenecks
   - Data flow and state management approaches
   - API design patterns (REST, GraphQL, gRPC)
   - Real-time vs batch processing considerations
   - Performance optimization strategies

4. **Compile Findings**:
   - Recommended architecture pattern with rationale
   - Scalability thresholds and considerations
   - Common pitfalls to avoid
   - References to case studies or whitepapers

**Limit**: 5-8 searches maximum, fetch 2-3 key resources

#### 2.3 Security & Compliance Research (WebSearch + WebFetch)

Research security best practices and compliance requirements for the domain:

1. **Search Compliance Requirements**:
   ```
   WebSearch("GDPR compliance [domain] applications 2026")
   WebSearch("HIPAA requirements [domain] 2026")  # if healthcare
   WebSearch("SOC2 compliance SaaS applications 2026")  # if B2B SaaS
   WebSearch("[domain] data privacy regulations 2026")
   ```

2. **Search Security Best Practices**:
   ```
   WebSearch("[domain] security best practices 2026")
   WebSearch("authentication authorization [use case] 2026")
   WebSearch("data encryption [domain] standards")
   ```

3. **Fetch Security Frameworks**:
   - If compliance standards are found, fetch detailed requirements
   - Look for security checklists and frameworks
   - Find audit requirements and validation processes

4. **Research Areas**:
   - Applicable compliance standards (GDPR, HIPAA, SOC2, PCI-DSS, etc.)
   - Data protection and privacy requirements
   - Authentication and authorization patterns
   - Encryption standards (at rest, in transit)
   - Audit logging requirements
   - Security testing and validation

5. **Compile Findings**:
   - List of applicable compliance requirements
   - Security framework recommendations
   - Data protection requirements
   - Common security vulnerabilities to address

**Limit**: 5-8 compliance/security searches, focus on most relevant

#### 2.4 Domain Knowledge Research (WebSearch + WebFetch)

Research domain-specific knowledge, scientific research, and market intelligence:

1. **Search Market Intelligence**:
   ```
   WebSearch("[product type] market size 2026")
   WebSearch("[domain] industry trends 2026")
   WebSearch("[use case] competitive landscape")
   WebSearch("leading [product type] competitors")
   ```

2. **Search Domain-Specific Research**:
   ```
   WebSearch("[domain] scientific research latest")
   WebSearch("[specific technique/methodology] best practices")
   WebSearch("[domain] expert recommendations")
   ```

3. **Fetch Academic/Industry Reports** (if applicable):
   - Use WebFetch for academic papers, industry reports, or expert analyses
   - Look for domain-specific methodologies or approaches
   - Find validation of problem space and solutions

4. **Research Areas**:
   - Market size and growth trends
   - Key competitors and their approaches
   - Target user demographics and behaviors
   - Domain-specific challenges and solutions
   - Scientific research supporting approach
   - Industry best practices and standards
   - Expert recommendations and thought leadership

5. **Compile Findings**:
   - Market size and opportunity estimates
   - Competitor analysis (3-5 main players)
   - Domain-specific insights and constraints
   - Scientific/expert validation of approach
   - User behavior patterns and preferences

**Limit**: 8-10 market/domain searches, fetch 2-4 key resources

#### 2.5 Research Synthesis

After completing all research phases, synthesize findings into a structured research report:

**Research Report Structure**:
```markdown
## Product Research Report

### Technology Research (Context7)
- Libraries/frameworks researched: [list]
- Recommended stack: [primary recommendations with reasons]
- Best practices found: [key practices]
- Version considerations: [compatibility notes]
- References: [Context7 queries performed]

### Architecture Research (WebSearch/WebFetch)
- Recommended architecture pattern: [pattern with rationale]
- Scalability considerations: [key points]
- Performance patterns: [optimization strategies]
- Case studies found: [relevant examples]
- References: [sources]

### Security & Compliance (WebSearch/WebFetch)
- Applicable compliance standards: [GDPR/HIPAA/SOC2/etc.]
- Security requirements: [authentication, encryption, etc.]
- Data protection needs: [privacy, residency, etc.]
- Risk areas identified: [potential vulnerabilities]
- References: [compliance sources]

### Domain Knowledge (WebSearch/WebFetch)
- Market opportunity: [size, growth, trends]
- Key competitors: [3-5 competitors with strengths/weaknesses]
- Target user insights: [demographics, behaviors, preferences]
- Domain-specific findings: [scientific research, expert insights]
- Problem validation: [confirmation of problem/solution fit]
- References: [market research sources]

### Research Gaps & Questions
- Information still needed from user: [list]
- Areas where research was inconclusive: [list]
- User-specific context required: [preferences, constraints, goals]
```

**Use Research to Inform Next Steps**:
- Identify which questions can be skipped (research answered them)
- Prepare smarter, more targeted questions based on research
- Pre-populate artifact sections with research findings
- Validate user assumptions against research

### 3. Gather Required Information (RESEARCH-INFORMED)

Use structured questions across 5 categories, **informed by research findings**. Skip questions that research fully answered. Focus on user-specific preferences, constraints, and goals that research couldn't determine.

**Question Strategy** (UPDATED):
- Review research report before asking questions
- Skip questions where research provides clear answers
- Ask validation questions to confirm research findings
- Focus on user preferences and constraints
- Reduce from 17 questions to typically 8-12 questions

Use the `AskUserQuestion` tool with multiple-choice options where appropriate.

**Question Strategy** (RESEARCH-INFORMED):
- Review research report before asking questions
- Skip questions where research provides clear, confident answers
- Ask validation questions to confirm research findings with user
- Focus on user preferences, constraints, and goals that research cannot determine
- Reduce from 17 questions to typically 8-12 questions based on research coverage
- Ask all Category 1 (Product Essence) questions if research doesn't fully answer them - these are CRITICAL
- Ask Category 2 (Market Context) questions for information research didn't confidently provide
- Ask Category 3-4 questions selectively, using research to inform options and skip obvious answers
- Infer Category 5 (Product Scope) answers when possible from research + briefing

**Category 1: Product Essence** (CRITICAL - always ask if missing)

Question 1: **What core problem does this product solve?**
**[May be informed by domain research]** - Domain knowledge research may have identified common problems in this space
- Prompt for specific, concrete problem statement
- Ask: "Describe the pain point in 2-3 sentences"
- Look for: Frequency, severity, current impact
- If research identified problems: Validate with user, ask for confirmation or clarification

Question 2: **Who experiences this problem?**
**[May be informed by market research]** - Market research may have identified target segments and user demographics
Options:
- Individual consumers (B2C)
- Small businesses (1-50 employees)
- Mid-market companies (50-500 employees)
- Enterprise organizations (500+ employees)
- Developers/technical users
- Specific vertical (healthcare, finance, education, etc.)
- Other (describe)
- If research identified segments: Present findings and ask for confirmation

Question 3: **How do people solve this problem today?**
**[May be informed by competitive research]** - Market research may have identified existing solutions and competitors
- Prompt for current solutions/workarounds
- Ask about limitations of existing solutions
- Look for: Gaps, frustrations, unmet needs
- If research identified solutions: Validate findings and ask about specific limitations user has experienced

Question 4: **What makes your solution different or better?**
**[Validate against competitive research]** - Research on competitors informs what differentiation is needed
- Prompt for unique value proposition
- Ask about competitive advantage or unfair advantage
- Look for: Differentiation, innovation, improvement
- If research identified competitors: Ask how user plans to differentiate from specific competitors found

**Category 2: Market Context** (HIGH PRIORITY)

Question 5: **What is your target user persona?**
**[Cross-reference with domain research]** - Domain research may provide insights into typical user roles and behaviors
- Prompt for detailed persona description
- Ask: "Describe your ideal user (role, goals, challenges)"
- Look for: Demographics, behaviors, motivations
- If research identified personas: Validate and ask user to refine with specific details

Question 6: **What's the market opportunity?**
**[Research may have preliminary data]** - Market research may have found TAM/SAM estimates and growth trends
Options:
- Small niche market (< $10M TAM)
- Growing niche ($10M-$100M TAM)
- Mid-size market ($100M-$1B TAM)
- Large established market ($1B-$10B TAM)
- Massive market (> $10B TAM)
- Unknown/need to research
- Not applicable (internal tool, side project, etc.)
- If research found market size: Present findings and ask for validation or refinement

Question 7: **Who are the main competitors or alternatives?**
**[Research may have identified some already]** - Competitive landscape research may have found major players
- Prompt for 3-5 key competitors or alternative solutions
- Ask about their strengths and weaknesses
- Look for: Market positioning opportunities
- If research identified competitors: Skip this question OR ask user to add any missing competitors and comment on findings

Question 8: **What's your unique positioning or unfair advantage?**
**[Validate against competitive landscape research]** - Competitive analysis informs what advantages are valuable in this market
Options:
- Deep domain expertise
- Proprietary technology or IP
- Unique data or insights
- Network effects or community
- Cost advantage or efficiency
- Superior UX/design
- Speed to market
- Strong partnerships or distribution
- Other (describe)
- If research identified competitive gaps: Suggest potential positioning based on findings

**Category 3: Technical Constraints** (MEDIUM PRIORITY)

Question 9: **Are there specific technical constraints or requirements?**
**[Research identifies relevant standards]** - Security research may have identified GDPR, HIPAA, SOC2, or other compliance needs
Options (multi-select):
- Must work on specific platform (web, mobile, desktop, embedded)
- Compliance requirements (HIPAA, SOC2, GDPR, etc.)
- Must integrate with specific systems
- Performance requirements (latency, throughput, scale)
- Offline/online requirements
- Security or privacy requirements
- Legacy system constraints
- None / flexible
- If research identified compliance requirements: Pre-select relevant options and ask user to confirm

Question 10: **Technology stack preferences?**
**[Research provides Context7-validated options]** - Technology research identifies best practices and recommended frameworks
Options:
- Modern web stack (React, Vue, Next.js, etc.)
- Mobile-first (React Native, Flutter, native iOS/Android)
- Backend-heavy (Node.js, Python, Go, Java, etc.)
- Full-stack monolith
- Microservices architecture
- Serverless / cloud-native
- No preference / open to recommendations
- Other (specify)
- If research suggests specific technologies: Present Context7-backed recommendations and ask for preferences

Question 11: **Expected scale and performance needs?**
**[Research provides architecture patterns]** - Architecture research suggests patterns for different scale levels
Options:
- Prototype / proof of concept (< 100 users)
- Small scale (100-1K users)
- Medium scale (1K-100K users)
- Large scale (100K-1M users)
- Very large scale (1M+ users)
- Unknown / will evolve
- Not a priority for MVP
- If research provides scale guidance: Recommend appropriate architecture patterns based on expected scale

**Category 4: Execution Context** (MEDIUM PRIORITY)

Question 12: **Timeline expectations for MVP?**
**[Research informs realistic estimates]** - Architecture and technology research helps set realistic timeline expectations
Options:
- Rapid prototype (2-4 weeks)
- Quick MVP (1-3 months)
- Standard MVP (3-6 months)
- Comprehensive MVP (6-12 months)
- Long-term project (12+ months)
- No specific timeline
- Other (specify)
- If research suggests complexity: Provide guidance on realistic timelines based on technical requirements

Question 13: **Team composition?**
**[Research suggests skill requirements]** - Technology research identifies required skills and team composition needs
Options:
- Solo developer/founder
- Small team (2-5 people)
- Medium team (6-15 people)
- Large team (15+ people)
- Will hire as needed
- Not yet determined
- If research identifies skill needs: Suggest required roles based on technology stack and architecture

Question 14: **Key success metrics?**
**[Research may suggest industry benchmarks]** - Domain research may identify standard success metrics for this product type
- Prompt for 2-4 measurable success metrics
- Ask: "How will you measure product success?"
- Look for: North star metric, KPIs, leading indicators
- Examples: User adoption, retention, revenue, engagement, NPS
- If research identifies benchmarks: Suggest industry-standard metrics and ask for user's priorities

**Category 5: Product Scope** (LOW PRIORITY - can infer if needed)

Question 15: **Core features for MVP?** (Optional)
**[Research identifies must-haves from domain analysis]** - Domain research shows what features are table stakes in this market
- Prompt for 3-7 must-have features for MVP
- Ask: "What features are absolutely essential for launch?"
- Look for: Minimal viable feature set
- If research identifies core features: Suggest must-have features based on competitive analysis and best practices

Question 16: **Future roadmap ideas?** (Optional)
**[Research suggests natural evolution]** - Technology and competitive research shows typical product evolution paths
- Prompt for 3-5 features for future phases
- Ask: "What comes after the MVP?"
- Look for: Growth and scale features
- If research suggests evolution: Propose typical growth features based on successful competitors and patterns

Question 17: **What's explicitly out of scope?** (Optional)
**[Research helps set boundaries]** - Competitive research shows what adjacent features might be tempting but dilute focus
- Prompt for features/capabilities to exclude
- Ask: "What won't this product do?"
- Look for: Boundary setting, focus areas
- If research identifies scope creep risks: Suggest boundaries based on successful focused competitors

### 3. Confirm Understanding

Before generating artifacts, confirm understanding with the user:

**Confirmation Format** (ENHANCED with research findings):
```
Let me confirm what I understand about your product:

**Product**: [Product name/description]
**Core Problem**: [Problem statement in 2-3 sentences]
**Target Users**: [User persona and market segment]
**Market Context**: [Market size, key competitors from research]
**Key Differentiation**: [Unique value proposition]
**Technical Approach**: [High-level architecture approach, informed by Context7 research]
**Compliance Requirements**: [GDPR, HIPAA, SOC2, etc. identified from research]
**MVP Timeline**: [Timeline expectation]
**Success Metrics**: [2-4 key metrics]

**Research Conducted**:
- Technology documentation: [Context7 libraries queried]
- Market/architecture research: [Key findings from WebSearch]
- Security/compliance: [Standards identified]
- Domain knowledge: [Insights from domain research]

Is this correct? Please confirm or provide corrections before I generate the product artifacts.
```

Wait for user confirmation. If corrections are needed, update understanding and re-confirm.

### 4. Generate Product Artifacts

Generate files in dependency order, showing progress after each file.

**Progress Format**:
```
Generating product artifacts...

✓ Created product vision (product.md) - [X] lines
⏳ Generating roadmap (roadmap.md)...
```

**Generation Sequence**:

**1. docs/product/product.md** (FIRST - foundation for all others)

Use the template in the "Content Templates" section below. Populate with:
- Product overview (name, status, last updated)
- Problem statement (from questions 1, 3)
- Our solution (from questions 4, 15)
- Target users (from questions 2, 5)
- Market opportunity (from questions 6, 7, 8)
- Product principles (infer from answers)
- Success metrics (from question 14)
- Vision timeline (from question 12, infer 6mo/1yr/3yr milestones)
- Risks and assumptions (infer from answers)

**Target**: 150-250 lines, comprehensive and actionable

**2. docs/product/roadmap.md** (SECOND - strategic planning)

Use the template in the "Content Templates" section below. Populate with:
- Roadmap overview (themes from product.md)
- Phase 1: MVP (from questions 12, 15 - 3-6 month plan)
- Phase 2: Growth (from question 16 - 6-12 month plan)
- Phase 3: Scale (infer from vision - 12+ month plan)
- Feature prioritization framework
- Dependencies and risks
- Deferred features (from question 17)
- Metrics and validation (from question 14)

**Target**: 200-250 lines, detailed roadmap with milestones

**3. docs/product/architecture.md** (THIRD - technical foundation)

Use the template in the "Content Templates" section below. Populate with:
- Architecture overview and principles
- Technology stack (from questions 10, 11 - be specific)
- System architecture (from questions 9, 10, 11, 15)
- Components and data model (infer from features)
- API design (infer from use cases)
- Cross-cutting concerns (from question 9 - security, performance, etc.)
- Development workflow
- Technical debt and future considerations

**Target**: 200-300 lines, comprehensive technical design

**4. docs/product/adr.md** (LAST - document decisions)

Use the template in the "Content Templates" section below. Create 2-4 ADRs:
- ADR-001: Technology Stack Selection (from questions 10, 11)
- ADR-002: Architecture Pattern Choice (monolith/microservices/serverless)
- ADR-003: Database/Storage Choice (infer from scale and data needs)
- ADR-004+: Any other critical decisions (optional)

Each ADR includes:
- Date, Status, Deciders
- Context (why this decision was needed)
- Decision (what was decided)
- Rationale (why this choice)
- Considered Alternatives (what else was considered)
- Consequences (positive, negative, neutral)
- Implementation Notes (if applicable)
- References (if applicable)

**Target**: 100-150 lines, document key architectural decisions

### 5. Update Working Context

After generating all product files, update `.context/` files following memory hierarchy pattern:

**Update .context/notes.md**:

Add a "Product Bootstrap Summary" section (< 150 lines):
```markdown
## Product Bootstrap Summary - [Product Name]

**Core Problem**: [2-3 sentences from product.md]
**Solution**: [2-3 sentences from product.md]
**Target Users**: [1-2 sentences from product.md]
**Technical Approach**: [2-3 sentences from architecture.md]
**MVP Timeline**: [1 sentence from roadmap.md]

**Key Constraints**:
- [Technical constraint from architecture.md]
- [Market constraint from product.md]
- [Resource constraint from roadmap.md]

**Research Conducted**:
- **Technology documentation**: [List Context7 libraries queried, e.g., "/facebook/react, /expressjs/express"]
- **Architecture patterns**: [Key architecture research findings from WebSearch]
- **Security/compliance**: [Standards identified: GDPR, HIPAA, SOC2, etc.]
- **Domain knowledge**: [Market size, competitors, industry insights from research]

**Key Research Findings**:
- [Finding 1 that influenced product direction]
- [Finding 2 that influenced technology choices]
- [Finding 3 that informed architecture decisions]

**Research Sources Summary**:
- Context7 queries: [Number] libraries documented
- WebSearch queries: [Number] searches across market/architecture/security
- WebFetch resources: [Number] deep-dive resources analyzed
- All artifacts include research citations for traceability

**Key Docs References**:
- docs/product/product.md - Full product vision and strategy (with market research citations)
- docs/product/roadmap.md - 12-month roadmap with 3 phases (with architecture research citations)
- docs/product/architecture.md - Technical architecture and design (with extensive Context7 references)
- docs/product/adr.md - Architectural decision records (with research-justified decisions)

**Next Steps**:
- Review generated artifacts and research citations
- Validate research findings against domain expertise
- Refine and customize as needed
- Begin development planning for Phase 1 (MVP)
```

**Update .context/changelog.md**:

Add a bootstrap entry (< 70 lines):
```markdown
## [Date] - Product Bootstrapping: [Product Name]

### Decisions
1. **Product focus**: [Core problem and solution]
2. **Technology stack**: [Key stack choices from ADR-001, informed by Context7 research]
3. **Architecture pattern**: [Pattern choice from ADR-002, validated by architecture research]
4. **Database choice**: [Database from ADR-003, backed by comparative research]
5. **Security/compliance**: [Compliance standards from ADR-004, identified from regulatory research]
6. **MVP scope**: [Timeline and core features from roadmap.md]
7. **Target market**: [User segment and market size from market research]

### Research Conducted
- **Context7 queries**: [List key libraries researched, e.g., "React, Express, PostgreSQL"]
- **Market research**: [Key market/competitive findings from WebSearch]
- **Architecture research**: [Key patterns/approaches researched]
- **Security research**: [Compliance standards identified: GDPR, HIPAA, SOC2, etc.]
- **Domain research**: [Domain-specific insights gathered]

### Artifacts Generated
- docs/product/product.md - Product vision (X lines) - WITH market research citations
- docs/product/roadmap.md - Product roadmap (X lines) - WITH architecture research citations
- docs/product/architecture.md - Technical architecture (X lines) - WITH extensive Context7 references
- docs/product/adr.md - Architecture decisions (X lines) - WITH research-justified decisions (4 ADRs)

### Rationale
[1-2 sentences on key reasoning for major decisions]

All decisions backed by research from Context7 (technology documentation), WebSearch (market/architecture/security), and WebFetch (deep-dive resources). See artifact Research Citations sections for full traceability.

### Next Actions
- Review and validate research citations in artifacts
- Refine product artifacts based on domain expertise
- Set up development environment per architecture.md
- Begin MVP development planning
```

**Update .context/handoff.md**:

Create comprehensive handoff:
```markdown
# Handoff - Product Bootstrapping Complete

## Session Context
- **Date**: [Today's date]
- **Activity**: Product bootstrapping via /bootstrap-product command
- **Product**: [Product name] - newly defined product vision

## What Was Accomplished

### Product Artifacts Generated
Successfully created comprehensive product documentation:
- ✓ **product.md** (X lines) - Product vision, problem statement, market opportunity, success metrics
- ✓ **roadmap.md** (X lines) - 12-month roadmap with 3 phases (MVP, Growth, Scale)
- ✓ **architecture.md** (X lines) - Technical architecture, stack choices, system design
- ✓ **adr.md** (X lines) - Documented key architectural decisions with rationale

### Information Gathered
Collected comprehensive product information through structured questioning:
- Product essence (problem, users, differentiation)
- Market context (target market, competitors, positioning)
- Technical constraints (platform, scale, compliance)
- Execution context (timeline, team, metrics)
- Product scope (MVP features, future roadmap)

### Research Conducted
Domain-expert research conducted BEFORE questioning to inform smarter questions and pre-populate artifacts:

**Context7 Technology Research**:
- [Library 1 researched with query used, e.g., "/facebook/react - best practices for state management"]
- [Library 2 researched with query used]
- [Library 3 researched with query used]
- Total: [X] Context7 libraries documented

**Market & Architecture Research (WebSearch)**:
- Market size and opportunity: [Key findings]
- Competitive landscape: [Competitors identified]
- Architecture patterns: [Patterns researched for this domain]
- Security/compliance: [Standards identified - GDPR, HIPAA, SOC2, etc.]
- Total: [Y] WebSearch queries across market/architecture/security

**Deep-Dive Research (WebFetch)**:
- [Whitepaper/guide 1 analyzed]
- [Academic paper or industry report 2]
- [Case study 3]
- Total: [Z] deep-dive resources analyzed

**Research Impact**:
- Questions reduced from 17 to [8-12 actual] based on research coverage
- All technology decisions backed by Context7 documentation
- All architectural decisions validated by industry research
- All compliance requirements identified proactively from research
- All artifacts include research citations for traceability

## Important Decisions Made

### 1. [Decision 1 - e.g., Technology Stack]
- **Decision**: [What was decided]
- **Rationale**: [Why this choice]
- **Reference**: docs/product/adr.md ADR-001

### 2. [Decision 2 - e.g., Architecture Pattern]
- **Decision**: [What was decided]
- **Rationale**: [Why this choice]
- **Reference**: docs/product/adr.md ADR-002

### 3. [Decision 3 - e.g., MVP Scope]
- **Decision**: [What was decided]
- **Rationale**: [Why this choice]
- **Reference**: docs/product/roadmap.md Phase 1

## Current State

### Completed
- ✓ Product vision fully defined
- ✓ 12-month roadmap established
- ✓ Technical architecture designed
- ✓ Architectural decisions documented
- ✓ Working context updated

### Ready for Next Session
- Product artifacts are comprehensive and actionable
- All files follow proper structure and format
- Cross-references between files are accurate
- .context/ files updated and under 500-line limits

## Next Steps

### Immediate (Next Session)
1. **Review product artifacts** - Read through all 4 generated files and refine as needed
2. **Validate market assumptions** - Research competitors and validate market opportunity
3. **Begin development planning** - Create initial sprint and user stories for MVP

### Soon
4. **Set up development environment** - Initialize project per architecture.md specifications
5. **Populate project management files** - Create backlog.md, current-sprint.md, current-story.md
6. **Start MVP development** - Begin Phase 1 implementation from roadmap.md

### Later
7. **Establish metrics tracking** - Implement success metrics from product.md
8. **Build roadmap Phase 2 features** - Expand beyond MVP
9. **Iterate based on user feedback** - Refine product vision and roadmap

## Context for Next Session

### Key Files to Be Aware Of
- **docs/product/product.md** - Core product vision (read first)
- **docs/product/roadmap.md** - Strategic roadmap and priorities
- **docs/product/architecture.md** - Technical design and stack
- **docs/product/adr.md** - Architectural decision rationale
- **.context/notes.md** - Product summary for quick reference

### Important Patterns Established
- Product vision is focused on [core problem/solution]
- Target market is [specific user segment]
- MVP timeline is [X months] with [Y core features]
- Technical approach follows [architecture pattern]
- Success measured by [key metrics]

### Gotchas & Things to Watch Out For
1. **[Constraint 1]**: [Description and mitigation]
2. **[Constraint 2]**: [Description and mitigation]
3. **MVP scope creep**: Stick to Phase 1 features only - resist adding to MVP

### Pending Decisions
1. **[Decision 1]**: [What needs to be decided and by when]
2. **[Decision 2]**: [What needs to be decided and by when]

## References

### Documentation
- docs/product/product.md - Full product vision
- docs/product/roadmap.md - 12-month strategic roadmap
- docs/product/architecture.md - Technical architecture and design
- docs/product/adr.md - All architectural decision records

### Related Context
- .context/notes.md - Product summary
- .context/changelog.md - Bootstrap decisions
- CLAUDE.md - Repository instructions and patterns

### Repository State
- Git status: [Current status]
- Branch: [Current branch]
- Commits: [New commits if any]

---

**Handoff Quality Check**:
- [x] Clear session context provided
- [x] All accomplishments documented
- [x] Important decisions captured with rationale
- [x] Current state is accurate
- [x] Next steps are actionable
- [x] Sufficient context for continuation
- [x] References are complete
- [x] Under 500 lines
```

**Verify .context/ file sizes**:
- Run `wc -l .context/*.md` to check line counts
- Ensure each file is under 500 lines
- If any file exceeds limit, summarize or archive older content

### 6. Provide Summary

After all files are generated and context is updated, provide a comprehensive summary to the user:

**Summary Format**:
```
## Product Bootstrapping Complete!

### Product Overview
- **Name**: [Product name]
- **Vision**: [One-sentence product vision]
- **Target**: [Target user segment]
- **MVP Timeline**: [Timeline]

### Generated Artifacts

**docs/product/product.md** (X lines)
- Product vision and value proposition
- Problem statement and target users
- Market opportunity and competitive landscape
- Success metrics and vision timeline

**docs/product/roadmap.md** (X lines)
- 12-month roadmap with 3 phases
- Phase 1 (MVP): [Timeline] - [Core features]
- Phase 2 (Growth): [Timeline] - [Growth features]
- Phase 3 (Scale): [Timeline] - [Scale features]

**docs/product/architecture.md** (X lines)
- Technology stack: [Key technologies]
- Architecture pattern: [Pattern]
- System components and data model
- Security, performance, and reliability considerations

**docs/product/adr.md** (X lines)
- ADR-001: Technology Stack Selection (with Context7 references)
- ADR-002: Architecture Pattern Choice (with architecture research)
- ADR-003: Database/Storage Choice (with comparative research)
- ADR-004: Security & Compliance Approach (with regulatory research)

### Research Conducted

**Technology Documentation (Context7)**:
- [X] libraries documented: [List key libraries, e.g., "React, Express, PostgreSQL"]
- All technology decisions backed by Context7 best practices

**Market & Competitive Research (WebSearch)**:
- [Y] searches conducted across market sizing, competitive analysis, architecture patterns
- Market size identified: [Size from research]
- Key competitors identified: [Competitors from research]
- Compliance requirements found: [GDPR, HIPAA, SOC2, etc.]

**Deep-Dive Research (WebFetch)**:
- [Z] whitepapers/guides/case studies analyzed
- Architecture patterns validated against industry best practices

**Research Impact**:
- Questions reduced from 17 to [actual number] based on research coverage
- All artifacts include research citations for traceability
- Decisions are research-backed, not assumptions

### Working Context Updated

✓ .context/notes.md - Product summary added
✓ .context/changelog.md - Bootstrap decisions recorded
✓ .context/handoff.md - Comprehensive handoff created
✓ All .context/ files under 500-line limits

### Next Steps

**Immediate**:
1. Review generated artifacts in `docs/product/`
2. Refine and customize as needed
3. Validate market assumptions and technical approach

**Soon**:
4. Set up development environment per architecture.md
5. Create project management files (backlog, sprint, stories)
6. Begin MVP development

Would you like to review any specific artifact or start development planning?
```

## Question Framework

The questions are organized into 5 categories with progressive disclosure:

**Category 1: Product Essence** - Questions 1-4 (CRITICAL, always ask if missing)
- Core problem
- Who has the problem
- Current solutions
- Differentiation

**Category 2: Market Context** - Questions 5-8 (HIGH PRIORITY)
- Target persona
- Market size/opportunity
- Competitors
- Unique positioning

**Category 3: Technical Constraints** - Questions 9-11 (MEDIUM PRIORITY)
- Platform/compliance constraints
- Technology preferences
- Scale and performance needs

**Category 4: Execution Context** - Questions 12-14 (MEDIUM PRIORITY)
- MVP timeline
- Team size
- Success metrics

**Category 5: Product Scope** - Questions 15-17 (LOW PRIORITY, can infer)
- MVP features
- Future features
- Out of scope

**Total**: 17 questions maximum, but use intelligent skipping:
- Skip questions if information is already provided in briefing
- Infer answers when reasonable (especially Category 5)
- Use multi-select for questions where multiple answers apply
- Always confirm understanding before generation (Step 3)

## Content Templates

### Template: product.md

```markdown
# [Product Name]

**Status**: Product Vision
**Last Updated**: [Date]
**Owner**: [Team/Person]

## Overview

[Product Name] is [one-sentence description of what the product is and does].

**Vision Statement**: [Aspirational 1-2 sentence statement of product's ultimate impact]

## Problem Statement

### The Problem

[Detailed description of the core problem being solved. Include:]
- What is the problem?
- How painful/frequent is it?
- What is the current impact?

### Who Has This Problem

**Primary User Persona**: [Persona name/description]
- **Role**: [Job title/role]
- **Goals**: [What they're trying to achieve]
- **Challenges**: [Key pain points they face]
- **Context**: [Where/when they encounter the problem]

**Market Segment**: [Target market segment from question 2]

**Market Size**: [Market opportunity from question 6]

### How They Solve It Today

[Description of current solutions and workarounds:]
- **Existing Solutions**: [List 2-4 current solutions]
- **Limitations**: [What's wrong with current solutions]
- **Gaps**: [What's missing in the market]

## Our Solution

### Value Proposition

[Product Name] solves this problem by [description of approach and benefits].

**Key Benefits**:
- [Benefit 1 - specific, measurable]
- [Benefit 2 - specific, measurable]
- [Benefit 3 - specific, measurable]

### How It Works

[High-level description of how the solution works, 2-4 paragraphs]

### Differentiation

**What Makes Us Different**:
- [Differentiator 1 - from question 4]
- [Differentiator 2 - from question 8]
- [Differentiator 3 - inferred]

**Our Unfair Advantage**: [From question 8 - why we can win]

## Market Opportunity

### Competitive Landscape

**Key Competitors**: [From question 7]
1. **[Competitor 1]**: [Strength/weakness]
2. **[Competitor 2]**: [Strength/weakness]
3. **[Competitor 3]**: [Strength/weakness]

**Alternative Solutions**: [Non-direct competitors or workarounds]

### Our Positioning

[Description of how we position against competitors - from questions 7, 8]

**Target Beachhead Market**: [Specific initial market segment to dominate]

## Product Principles

[Core values and design philosophy that guide product decisions, 4-6 principles:]
1. **[Principle 1]**: [Description]
2. **[Principle 2]**: [Description]
3. **[Principle 3]**: [Description]
4. **[Principle 4]**: [Description]

## Success Metrics

**North Star Metric**: [Primary metric that indicates product success - from question 14]

**Key Performance Indicators**:
- [KPI 1 with target]
- [KPI 2 with target]
- [KPI 3 with target]
- [KPI 4 with target]

**Leading Indicators**: [Early signals that predict success]

## Vision Timeline

### 6 Months (MVP)
[What we'll achieve in 6 months - from question 12 and roadmap Phase 1]

### 1 Year (Growth)
[What we'll achieve in 1 year - from roadmap Phase 2]

### 3 Years (Scale)
[Long-term vision - where we want to be in 3 years]

## Risks & Assumptions

### Key Assumptions
[Critical assumptions that must be true for success:]
1. [Assumption 1]
2. [Assumption 2]
3. [Assumption 3]

### Key Risks
[Major risks and mitigation strategies:]
1. **[Risk 1]**: [Description] | **Mitigation**: [Strategy]
2. **[Risk 2]**: [Description] | **Mitigation**: [Strategy]
3. **[Risk 3]**: [Description] | **Mitigation**: [Strategy]

## Research Citations

**Market Research**:
- [WebSearch query results for market size/opportunity]
- [Domain research sources for industry trends]
- [Relevant URLs from WebFetch for market analysis]

**Competitive Analysis**:
- [WebSearch findings on competitors and alternatives]
- [URLs to competitor analysis or market reports]

**Domain Knowledge**:
- [Scientific research or academic papers from WebFetch]
- [Industry reports or whitepapers]
- [Expert analyses or case studies]

*Note: Include specific Context7 library IDs, WebSearch queries used, and URLs fetched for transparency and future reference.*

## Open Questions

[Questions that still need to be answered:]
- [Question 1]
- [Question 2]
- [Question 3]

---

*This product vision document should be reviewed and updated quarterly.*
```

### Template: roadmap.md

```markdown
# Product Roadmap

**Product**: [Product Name]
**Last Updated**: [Date]
**Planning Horizon**: 12 months

## Roadmap Overview

**Vision Alignment**: [How this roadmap supports the product vision]

**Key Themes**: [3-4 strategic themes that guide the roadmap]
1. [Theme 1]
2. [Theme 2]
3. [Theme 3]

**Roadmap Principles**:
- [Principle 1 - e.g., "Focus on MVP first"]
- [Principle 2 - e.g., "Validate with users before building"]
- [Principle 3 - e.g., "Measure impact of every feature"]

## Phase 1: MVP (Months 1-[X])

**Timeline**: [Start] - [End]
**Goal**: [Primary goal of MVP phase]
**Status**: Planning

### Objectives
- [Objective 1 - measurable]
- [Objective 2 - measurable]
- [Objective 3 - measurable]

### Core Features

**Must Have** (MVP Critical):
1. **[Feature 1]** - [Description and value]
2. **[Feature 2]** - [Description and value]
3. **[Feature 3]** - [Description and value]
4. **[Feature 4]** - [Description and value]

[Add from question 15 - core MVP features]

**Should Have** (Important but can defer):
- [Feature X] - [Description]
- [Feature Y] - [Description]

### Success Criteria
- [Criterion 1 - from question 14]
- [Criterion 2 - from question 14]
- [Criterion 3 - from question 14]

### Dependencies & Risks
**Dependencies**:
- [Dependency 1]
- [Dependency 2]

**Risks**:
- [Risk 1] | **Mitigation**: [Strategy]
- [Risk 2] | **Mitigation**: [Strategy]

## Phase 2: Growth (Months [X]-[Y])

**Timeline**: [Start] - [End]
**Goal**: [Primary goal of Growth phase]
**Status**: Planned

### Objectives
- [Objective 1 - focus on growth/adoption]
- [Objective 2 - focus on retention/engagement]
- [Objective 3 - focus on optimization]

### Growth Features

**High Priority**:
1. **[Feature 1]** - [Description and growth impact]
2. **[Feature 2]** - [Description and growth impact]
3. **[Feature 3]** - [Description and growth impact]

[Add from question 16 - future roadmap ideas]

**Medium Priority**:
- [Feature X] - [Description]
- [Feature Y] - [Description]

### Success Criteria
- [Growth metric 1 with target]
- [Growth metric 2 with target]
- [Growth metric 3 with target]

## Phase 3: Scale (Months [Y]+)

**Timeline**: [Start] - [End]
**Goal**: [Primary goal of Scale phase]
**Status**: Conceptual

### Objectives
- [Objective 1 - focus on scale/performance]
- [Objective 2 - focus on enterprise/advanced features]
- [Objective 3 - focus on platform/ecosystem]

### Scale Features

**Potential Features**:
1. **[Feature 1]** - [Description and scale impact]
2. **[Feature 2]** - [Description and scale impact]
3. **[Feature 3]** - [Description and scale impact]

[Infer from product vision and market opportunity]

### Success Criteria
- [Scale metric 1 with target]
- [Scale metric 2 with target]
- [Scale metric 3 with target]

## Feature Prioritization Framework

**Prioritization Criteria**:
1. **Impact**: [How we measure impact]
2. **Effort**: [How we estimate effort]
3. **Confidence**: [How we assess confidence]
4. **Strategic Value**: [How we evaluate strategic fit]

**Priority Levels**:
- **P0**: Critical for success, must have
- **P1**: High value, should have soon
- **P2**: Nice to have, can defer
- **P3**: Low priority or research needed

## Deferred Features

**Features Not in Current Roadmap**: [From question 17]
- [Feature 1] - **Reason**: [Why deferred]
- [Feature 2] - **Reason**: [Why deferred]
- [Feature 3] - **Reason**: [Why deferred]

**Out of Scope**:
- [Feature X] - **Reason**: [Why out of scope]
- [Feature Y] - **Reason**: [Why out of scope]

## Dependencies & Constraints

**External Dependencies**:
- [Dependency 1 - e.g., third-party API, partnership]
- [Dependency 2]

**Technical Dependencies**:
- [Dependency 1 - e.g., infrastructure, tooling]
- [Dependency 2]

**Resource Constraints**: [From questions 12, 13]
- Team size: [X people]
- Timeline: [Y months for MVP]
- Budget: [If applicable]

## Metrics & Validation

**How We Measure Success**: [From question 14]

**Phase 1 Metrics**:
- [Metric 1]: Target [X] by [Date]
- [Metric 2]: Target [X] by [Date]

**Phase 2 Metrics**:
- [Metric 1]: Target [X] by [Date]
- [Metric 2]: Target [X] by [Date]

**Validation Approach**:
- [How we'll validate each phase - user testing, beta, analytics, etc.]

## Roadmap Assumptions

**Critical Assumptions**:
1. [Assumption 1 that roadmap depends on]
2. [Assumption 2 that roadmap depends on]
3. [Assumption 3 that roadmap depends on]

**What Could Change This Roadmap**:
- [Factor 1 - e.g., user feedback, market changes]
- [Factor 2]
- [Factor 3]

## Research Citations

**Architecture Patterns**:
- [WebSearch findings on scalability approaches for this domain]
- [Architecture pattern research from WebFetch - whitepapers, case studies]
- [Industry best practices for phased rollout]

**Technology Research**:
- [Context7 library documentation used for timeline estimates]
- [Technology maturity and ecosystem research]

**Domain Research**:
- [Competitive product roadmap analysis]
- [Industry trend research informing feature priorities]

*Note: Include specific WebSearch queries, URLs fetched, and Context7 library IDs for transparency.*

---

*This roadmap is reviewed monthly and updated quarterly.*
```

### Template: architecture.md

```markdown
# Technical Architecture

**Product**: [Product Name]
**Last Updated**: [Date]
**Status**: Design

## Architecture Overview

**System Vision**: [High-level description of technical approach]

**Architecture Principles**:
1. [Principle 1 - e.g., "Simplicity over complexity"]
2. [Principle 2 - e.g., "Security by design"]
3. [Principle 3 - e.g., "Build for current scale, design for future scale"]
4. [Principle 4 - e.g., "Developer experience matters"]

**Target Scale**: [From question 11 - expected users/load]

## Technology Stack

### Frontend

**Framework**: [From question 10]
- [Primary framework choice]
- [Supporting libraries]
- [Rationale in 1 sentence]

**UI Components**:
- [Component library or custom]
- [Styling approach]

**State Management**:
- [Approach - Redux, Context, etc.]

**Build Tools**:
- [Build system]
- [Package manager]

### Backend

**Framework**: [From question 10]
- [Primary framework/language]
- [Web server/runtime]
- [Rationale in 1 sentence]

**API Design**:
- [REST, GraphQL, gRPC, etc.]
- [Authentication approach]
- [API versioning strategy]

**Key Libraries**:
- [Library 1 - purpose]
- [Library 2 - purpose]
- [Library 3 - purpose]

### Database

**Primary Database**: [From architecture decisions]
- [Database type and technology]
- [Schema approach]
- [Rationale in 1 sentence]

**Caching**:
- [Caching strategy if needed]

**Data Storage**:
- [File storage approach if needed]
- [Object storage if needed]

### Infrastructure

**Hosting**: [From question 10, 11]
- [Cloud provider or on-prem]
- [Deployment model]

**CI/CD**:
- [Build pipeline]
- [Deployment automation]

**Monitoring & Observability**:
- [Logging approach]
- [Metrics/monitoring tools]
- [Error tracking]

### Third-Party Services

**Integrations**: [From question 9]
1. **[Service 1]**: [Purpose and why]
2. **[Service 2]**: [Purpose and why]
3. **[Service 3]**: [Purpose and why]

**Authentication/Authorization**:
- [Auth provider if using third-party]

## System Architecture

### High-Level Architecture

[Text description of architecture pattern - from ADR-002]
- [Architecture type: monolith, microservices, serverless, etc.]
- [Key components and their responsibilities]
- [Communication patterns between components]
- [Data flow overview]

### Component Architecture

**Frontend Components**:
```
[Component tree or key component descriptions]
- [Component 1]: [Responsibility]
- [Component 2]: [Responsibility]
- [Component 3]: [Responsibility]
```

**Backend Components**:
```
[Service/module breakdown]
- [Service 1]: [Responsibility]
- [Service 2]: [Responsibility]
- [Service 3]: [Responsibility]
```

### Data Model

**Core Entities**: [From features in questions 15, 16]

1. **[Entity 1]**
   - [Key attributes]
   - [Relationships]
   - [Purpose]

2. **[Entity 2]**
   - [Key attributes]
   - [Relationships]
   - [Purpose]

3. **[Entity 3]**
   - [Key attributes]
   - [Relationships]
   - [Purpose]

**Data Relationships**:
[Description of how entities relate]

### API Design

**Endpoints** (MVP):

```
[List key API endpoints for MVP features]

User Management:
- POST /api/auth/signup
- POST /api/auth/login
- GET /api/user/profile

[Feature 1 APIs]:
- GET /api/[resource]
- POST /api/[resource]
- PUT /api/[resource]/:id
- DELETE /api/[resource]/:id

[Continue for core features...]
```

**API Patterns**:
- [RESTful conventions followed]
- [Error handling approach]
- [Pagination strategy]
- [Rate limiting approach]

## Cross-Cutting Concerns

### Security

**Security Requirements**: [From question 9]
- [Compliance requirements if any]
- [Data privacy requirements]
- [Security certifications needed]

**Security Measures**:
- **Authentication**: [Approach and implementation]
- **Authorization**: [RBAC, ABAC, etc.]
- **Data Encryption**: [In transit and at rest]
- **Input Validation**: [Validation strategy]
- **OWASP Top 10**: [How we address each]

### Performance

**Performance Requirements**: [From question 11]
- [Latency targets]
- [Throughput targets]
- [Concurrent users target]

**Performance Strategies**:
- [Caching strategy]
- [Database indexing approach]
- [CDN usage if applicable]
- [Code optimization areas]

### Reliability

**Availability Target**: [SLA goal]

**Reliability Measures**:
- [Error handling strategy]
- [Retry mechanisms]
- [Fallback strategies]
- [Data backup approach]
- [Disaster recovery plan]

### Scalability

**Current Scale**: [From question 11]
**Future Scale**: [From question 11]

**Scalability Strategy**:
- [Horizontal vs vertical scaling approach]
- [Database scaling strategy]
- [Caching for scale]
- [Async processing if needed]

### Observability

**Logging**:
- [Logging framework]
- [Log levels and structure]
- [Log aggregation]

**Metrics**:
- [Key metrics to track]
- [Monitoring tools]
- [Alerting strategy]

**Tracing**:
- [Distributed tracing if applicable]
- [Performance profiling]

## Development Workflow

### Local Development

**Setup Requirements**:
- [Prerequisites]
- [Environment setup steps]
- [Configuration needed]

**Development Tools**:
- [IDE recommendations]
- [Code formatting]
- [Linting]
- [Git hooks]

### Testing Strategy

**Test Levels**:
- **Unit Tests**: [Framework and coverage target]
- **Integration Tests**: [Approach]
- **End-to-End Tests**: [Framework if applicable]
- **Performance Tests**: [When and how]

**Test Automation**:
- [CI pipeline integration]
- [Test coverage requirements]

### Deployment

**Environments**:
- Development
- Staging
- Production

**Deployment Process**:
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Rollback procedure]

**Release Strategy**:
- [Versioning approach]
- [Release frequency]
- [Feature flags if used]

## Technical Debt & Future Considerations

### Known Limitations

[Technical limitations or trade-offs made for MVP:]
1. [Limitation 1] - **Impact**: [Impact] | **Plan**: [When to address]
2. [Limitation 2] - **Impact**: [Impact] | **Plan**: [When to address]
3. [Limitation 3] - **Impact**: [Impact] | **Plan**: [When to address]

### Technical Debt

[Intentional technical debt being taken on:]
- [Debt 1] - **Reason**: [Why] | **Payback Plan**: [When/how]
- [Debt 2] - **Reason**: [Why] | **Payback Plan**: [When/how]

### Future Technical Considerations

[Technical work planned for Phase 2/3:]
- [Consideration 1 - e.g., "Migration to microservices"]
- [Consideration 2 - e.g., "GraphQL API layer"]
- [Consideration 3 - e.g., "Real-time capabilities"]

## Dependencies & Integration

**External Dependencies**:
- [Dependency 1 and purpose]
- [Dependency 2 and purpose]

**Integration Points**:
- [Integration 1] - **Type**: [API, webhook, etc.]
- [Integration 2] - **Type**: [API, webhook, etc.]

**Platform Requirements**: [From question 9]
- [Platform 1 - e.g., "Must run on iOS 14+"]
- [Platform 2 - e.g., "Web browsers: Chrome, Firefox, Safari"]

## Research Citations

**Technology Documentation (Context7)**:
- **Frontend Framework**: [Context7 library ID for chosen framework, e.g., /facebook/react]
  - Query: [Best practices query used]
  - Key findings: [Summary of relevant documentation]
- **Backend Framework**: [Context7 library ID, e.g., /expressjs/express]
  - Query: [Best practices query used]
  - Key findings: [Summary]
- **Database Technology**: [Context7 library ID if available]
  - Query: [Query used]
  - Key findings: [Summary]
- **Additional Libraries**: [List all Context7 queries made with library IDs]

**Architecture Patterns**:
- [WebSearch query for architecture pattern research]
- [WebFetch URL for architecture whitepapers or case studies]
- [Industry best practices for this type of system]

**Security Best Practices**:
- [WebSearch findings on GDPR/HIPAA/SOC2 compliance]
- [Security framework documentation URLs]
- [OWASP guidelines and resources]

**Scalability Research**:
- [WebSearch findings on scaling patterns for this domain]
- [Case studies or benchmarks from WebFetch]
- [Performance optimization guides]

**Technology Evaluation**:
- [Comparative research between technology choices]
- [Community adoption and maturity metrics]
- [Ecosystem and tooling availability]

*Note: All technology stack decisions are backed by Context7 documentation queries. Include specific library IDs (/org/project format), queries used, and key findings for complete traceability and future reference.*

---

*This architecture document should be reviewed before major technical decisions and updated as the system evolves.*
```

### Template: adr.md

```markdown
# Architecture Decision Records (ADR)

This document contains all architecture decision records for [Product Name].

**ADR Format**: We follow the [MADR format](https://adr.github.io/madr/) for documenting decisions.

---

## ADR-001: Technology Stack Selection

**Date**: [Date]
**Status**: Accepted
**Deciders**: [Team/Person]

### Context

We need to select a technology stack for [Product Name] that supports our MVP goals and can scale as the product grows. Key considerations include:
- Development speed for MVP timeline ([X months] from question 12)
- Team expertise and hiring considerations ([Team size] from question 13)
- Target scale ([User count] from question 11)
- Platform requirements ([Platform] from question 9)
- Technical constraints ([Constraints] from question 9)

### Decision

We will use the following technology stack:

**Frontend**:
- [Framework choice from question 10]
- [Key supporting libraries]

**Backend**:
- [Language/framework choice from question 10]
- [Runtime/server choice]

**Database**:
- [Database choice - see ADR-003]

**Infrastructure**:
- [Cloud provider and deployment approach]

### Rationale

**Why this stack**:
1. [Reason 1 - e.g., "Fast MVP development with React ecosystem"]
2. [Reason 2 - e.g., "Team has expertise in Node.js"]
3. [Reason 3 - e.g., "Proven at target scale of 100K users"]
4. [Reason 4 - e.g., "Strong community and libraries"]

**Alignment with requirements**:
- [How it meets requirement 1 from questions]
- [How it meets requirement 2 from questions]
- [How it meets requirement 3 from questions]

### Considered Alternatives

**Alternative 1**: [Alternative stack]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]

**Alternative 2**: [Alternative stack]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]

### Consequences

**Positive**:
- [Positive consequence 1]
- [Positive consequence 2]
- [Positive consequence 3]

**Negative**:
- [Negative consequence 1 - trade-off]
- [Negative consequence 2 - limitation]

**Neutral**:
- [Neutral consequence 1 - just a fact]

### Implementation Notes

[Any important notes for implementation]
- [Note 1]
- [Note 2]

### References

**Context7 Documentation**:
- [Context7 library ID for frontend framework with query used]
- [Context7 library ID for backend framework with query used]
- [Context7 library ID for key libraries with queries used]

**Technology Comparisons**:
- [WebSearch query for technology comparison research]
- [URLs to benchmark or comparison articles from WebFetch]

**Best Practices**:
- [Context7 best practices findings]
- [Industry standard references]

**Internal**:
- [Team discussion or decision meeting notes]

*All technology choices backed by Context7 documentation queries and comparative research.*

---

## ADR-002: Architecture Pattern Choice

**Date**: [Date]
**Status**: Accepted
**Deciders**: [Team/Person]

### Context

We need to decide on the overall architecture pattern for [Product Name]. Key considerations include:
- MVP timeline and development speed ([X months])
- Expected scale ([User count] from question 11)
- Team size and structure ([Team size] from question 13)
- System complexity based on features
- Future scalability needs

### Decision

We will use a **[Monolith / Microservices / Serverless / Hybrid]** architecture.

[For monolith]: Single application with modular internal structure
[For microservices]: Service-oriented with [N] initial services
[For serverless]: Function-based with [cloud provider] functions
[For hybrid]: [Description of hybrid approach]

### Rationale

**Why this pattern**:
1. [Reason 1 - e.g., "Monolith allows faster MVP development"]
2. [Reason 2 - e.g., "Current scale doesn't justify microservices complexity"]
3. [Reason 3 - e.g., "Aligns with team size and expertise"]
4. [Reason 4 - e.g., "Can migrate to microservices in Phase 3 if needed"]

### Considered Alternatives

**Alternative 1**: [Alternative pattern]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason - e.g., "Premature optimization"]

**Alternative 2**: [Alternative pattern]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]

### Consequences

**Positive**:
- [Positive consequence 1]
- [Positive consequence 2]

**Negative**:
- [Negative consequence 1]
- [Negative consequence 2]

**Neutral**:
- [Neutral consequence 1]

### Migration Path

[If applicable, describe future migration path]
- Phase 1 (MVP): [Current pattern]
- Phase 2: [Potential evolution]
- Phase 3: [Potential migration to different pattern]

### Implementation Notes

[Architecture implementation guidelines]
- [Guideline 1 - e.g., "Maintain clear module boundaries"]
- [Guideline 2 - e.g., "Design for future extraction if needed"]

### References

**Architecture Pattern Research**:
- [WebSearch queries for architecture pattern research and best practices]
- [URLs to architecture whitepapers or case studies from WebFetch]
- [Industry examples of similar systems]

**Scalability Research**:
- [WebSearch findings on scaling this pattern]
- [Case studies from companies at similar scale]

**Context7 Documentation**:
- [Framework documentation supporting chosen pattern]

*Decision informed by architecture research and industry best practices.*

---

## ADR-003: Database/Storage Choice

**Date**: [Date]
**Status**: Accepted
**Deciders**: [Team/Person]

### Context

We need to select a database solution that supports our data model, scale requirements, and development timeline. Key considerations include:
- Data model complexity [from features]
- Expected data volume and query patterns
- Target scale ([User count] from question 11)
- Team expertise
- ACID vs eventual consistency needs
- Budget constraints

### Decision

We will use **[Database choice]** as our primary database.

[Specify: PostgreSQL, MySQL, MongoDB, DynamoDB, Firebase, etc.]

**Additional storage**:
- [If needed: cache layer, file storage, etc.]

### Rationale

**Why this database**:
1. [Reason 1 - e.g., "Relational model fits our data structure"]
2. [Reason 2 - e.g., "Strong ACID guarantees needed for transactions"]
3. [Reason 3 - e.g., "Proven at target scale"]
4. [Reason 4 - e.g., "Team has PostgreSQL expertise"]
5. [Reason 5 - e.g., "Excellent ecosystem and tooling"]

### Considered Alternatives

**Alternative 1**: [Alternative database]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]

**Alternative 2**: [Alternative database]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]

### Consequences

**Positive**:
- [Positive consequence 1]
- [Positive consequence 2]

**Negative**:
- [Negative consequence 1 - trade-off]
- [Negative consequence 2 - limitation]

**Neutral**:
- [Neutral consequence 1]

### Schema Design

**Approach**: [Normalized/Denormalized/Hybrid]

**Key Design Decisions**:
- [Decision 1 - e.g., "User data in separate table"]
- [Decision 2 - e.g., "JSONB for flexible metadata"]
- [Decision 3 - e.g., "Indexing strategy for performance"]

### Implementation Notes

[Database-specific implementation guidelines]
- [Note 1 - e.g., "Use migrations for schema changes"]
- [Note 2 - e.g., "Connection pooling configuration"]
- [Note 3 - e.g., "Backup and recovery procedures"]

### References

**Context7 Documentation**:
- [Context7 library ID for database technology if available]
- [ORM or database client library documentation]

**Database Comparisons**:
- [WebSearch queries for database comparison research]
- [URLs to benchmark or performance comparison articles]

**Best Practices**:
- [Schema design best practices from research]
- [Scaling and performance optimization guides]

**Use Case Research**:
- [Similar product database choices from research]
- [Industry standard for this type of application]

*Database choice validated through Context7 documentation and comparative performance research.*

---

## ADR-004: Security & Compliance Approach

**Date**: [Date]
**Status**: Accepted
**Deciders**: [Team/Person]

### Context

We need to establish security and compliance requirements for [Product Name]. Key considerations include:
- Regulatory compliance requirements ([GDPR, HIPAA, SOC2, etc.] from question 9 and research)
- Data privacy and protection needs
- Target market requirements (especially for B2B/Enterprise)
- Security best practices for [domain/industry]
- User data handling and storage requirements

### Decision

We will implement the following security and compliance framework:

**Compliance Standards**:
- [Standard 1 - e.g., "GDPR compliance for EU users"]
- [Standard 2 - e.g., "SOC 2 Type II certification"]
- [Standard 3 - e.g., "HIPAA compliance for healthcare data"]

**Security Measures**:
- [Measure 1 - e.g., "End-to-end encryption for sensitive data"]
- [Measure 2 - e.g., "Multi-factor authentication"]
- [Measure 3 - e.g., "Regular security audits and penetration testing"]
- [Measure 4 - e.g., "OWASP Top 10 mitigation"]

### Rationale

**Why this approach**:
1. [Reason 1 - e.g., "GDPR required for EU market expansion"]
2. [Reason 2 - e.g., "Enterprise customers require SOC 2"]
3. [Reason 3 - e.g., "Industry best practices for data protection"]
4. [Reason 4 - e.g., "Builds user trust and competitive advantage"]

**Alignment with requirements**:
- [How it meets compliance requirement 1 from research]
- [How it meets compliance requirement 2 from research]
- [How it addresses security concerns from domain]

### Considered Alternatives

**Alternative 1**: [Alternative approach - e.g., "Minimal compliance, add later"]
- **Pros**: [Benefits - e.g., "Faster MVP"]
- **Cons**: [Drawbacks - e.g., "Limits market, harder to retrofit"]
- **Why not chosen**: [Reason - e.g., "Compliance needed from day 1 for target market"]

**Alternative 2**: [Alternative approach]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]

### Consequences

**Positive**:
- [Positive consequence 1 - e.g., "Can sell to enterprise customers"]
- [Positive consequence 2 - e.g., "Reduces security risk"]
- [Positive consequence 3 - e.g., "Builds user trust"]

**Negative**:
- [Negative consequence 1 - e.g., "Increases development complexity"]
- [Negative consequence 2 - e.g., "Higher operational costs"]

**Neutral**:
- [Neutral consequence 1 - e.g., "Requires ongoing compliance monitoring"]

### Implementation Notes

**GDPR Requirements** (if applicable):
- Right to access, rectification, erasure
- Data portability
- Consent management
- Data processing agreements

**Security Implementation**:
- [Implementation note 1 - e.g., "Use industry-standard encryption libraries"]
- [Implementation note 2 - e.g., "Implement audit logging for all data access"]
- [Implementation note 3 - e.g., "Regular security training for team"]

### References

**Compliance Research**:
- [WebSearch findings on GDPR/HIPAA/SOC2 requirements]
- [URLs to official compliance documentation]
- [Compliance framework guides from WebFetch]

**Security Best Practices**:
- [OWASP Top 10 guidelines]
- [Industry-specific security standards]
- [Security framework documentation]

**Context7 Documentation**:
- [Security libraries and tools documentation]
- [Authentication/authorization framework documentation]

**Domain-Specific Research**:
- [Industry security requirements from research]
- [Data protection standards for this domain]

*Security and compliance approach informed by regulatory research and industry best practices.*

---

## ADR Template (for future decisions)

**Date**: YYYY-MM-DD
**Status**: [Proposed | Accepted | Deprecated | Superseded]
**Deciders**: [List of people involved]

### Context

[Describe the context and problem statement]
- What is the issue we're addressing?
- What factors are influencing this decision?
- What constraints do we have?

### Decision

[Describe the decision that was made]

### Rationale

[Explain why this decision was made]
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

### Considered Alternatives

**Alternative 1**: [Name]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Why not chosen**: [Reason]

[Add more alternatives as needed]

### Consequences

**Positive**:
- [Positive consequence 1]
- [Positive consequence 2]

**Negative**:
- [Negative consequence 1]
- [Negative consequence 2]

**Neutral**:
- [Neutral consequence 1]

### Implementation Notes

[Any important notes for implementing this decision]

### References

[Links to supporting documentation, discussions, or research]

---

*ADRs should be added whenever a significant architectural decision is made. Number them sequentially (ADR-004, ADR-005, etc.).*
```

## Important Guidelines

**DO**:
- Ask comprehensive questions to gather rich information
- Confirm understanding before generating artifacts
- Generate files in dependency order (product → roadmap → architecture → adr)
- Show progress after each file generation
- Create detailed, specific content (not generic placeholders)
- Make content actionable and realistic
- Update all `.context/` files after generation
- Verify `.context/` files stay under 500 lines
- Cross-reference between generated files
- Include rationale for all major decisions
- Create a comprehensive handoff for next session
- Use the templates as guides, not rigid constraints

**DON'T**:
- Generate files before confirming understanding with user
- Create generic template content without specific details
- Generate files in wrong order (dependencies matter)
- Skip updating `.context/` files
- Create `.context/` files exceeding 500 lines
- Forget to show progress during generation
- Use vague or aspirational language without concrete details
- Skip the question-asking phase (unless briefing is comprehensive)
- Generate all files silently - communicate progress
- Make assumptions about technical choices without basis in answers
- Create unrealistic timelines or scope

**Goal**: Transform a product briefing into comprehensive, market-viable product documentation that provides a clear vision, strategic roadmap, technical architecture, and decision rationale. The artifacts should enable immediate transition to development planning with confidence that the product direction is well-defined and achievable.

---

**Quality Checklist** (Verify before marking complete):
- [ ] All 4 files generated with correct names and locations
- [ ] Files follow template structure consistently
- [ ] Content is specific to the product (not generic)
- [ ] Product vision clearly articulates problem, solution, value
- [ ] Target users and market are well-defined
- [ ] Roadmap has realistic phases with measurable milestones
- [ ] Architecture addresses all technical concerns (security, scale, performance)
- [ ] ADRs document key architectural decisions with clear rationale
- [ ] Cross-references between files are accurate
- [ ] `.context/notes.md` updated with product summary (< 100 lines)
- [ ] `.context/changelog.md` updated with bootstrap entry (< 50 lines)
- [ ] `.context/handoff.md` created with comprehensive handoff
- [ ] All `.context/` files verified under 500-line limits
- [ ] Summary provided to user with next steps

**Success Metrics**: After running this command, the user should have a complete product vision ready for development, with all necessary artifacts to begin building confidently.
