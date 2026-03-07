#!/usr/bin/env python3
"""
Cloud & Email Lookup Tool - Enterprise Edition
Professional domain intelligence platform
"""

import streamlit as st
import socket
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import io

# Page config
st.set_page_config(
    page_title="Cloud & Email Lookup Tool",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional Corporate CSS
st.markdown("""
<style>
    /* Clean professional design */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Top header */
    .main-header {
        background: #1e3a5f;
        color: white;
        padding: 1.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 3px solid #2c5282;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 1.75rem;
        font-weight: 600;
        letter-spacing: -0.025em;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 0.95rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Professional stats cards */
    .stat-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.25rem;
        font-weight: 700;
        color: #1e3a5f;
        margin: 0;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Clean sections */
    .section {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Professional buttons */
    .stButton>button {
        background: #1e3a5f;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.025em;
        transition: background 0.2s ease;
    }
    
    .stButton>button:hover {
        background: #2c5282;
    }
    
    /* Clean tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: transparent;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: #64748b;
        font-weight: 500;
        padding: 0.75rem 0;
        font-size: 0.95rem;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: transparent;
        color: #1e3a5f;
        border-bottom: 2px solid #1e3a5f;
    }
    
    /* Professional data table */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 4px;
    }
    
    /* Clean file uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #cbd5e0;
        border-radius: 4px;
        padding: 2rem;
        background: #f8fafc;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: #1e3a5f;
    }
    
    /* Info boxes */
    .info-box {
        background: #f0f9ff;
        border-left: 4px solid #1e3a5f;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    
    .how-it-works {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .how-it-works h3 {
        color: #1e293b;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 1rem 0;
    }
    
    .how-it-works ol {
        margin: 0;
        padding-left: 1.5rem;
        color: #475569;
        line-height: 1.8;
    }
    
    .how-it-works li {
        margin-bottom: 0.5rem;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Professional badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 3px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .badge-azure { background: #0078D4; color: white; }
    .badge-aws { background: #FF9900; color: white; }
    .badge-gcp { background: #4285F4; color: white; }
    .badge-high { background: #059669; color: white; }
    .badge-medium { background: #d97706; color: white; }
    .badge-low { background: #dc2626; color: white; }
</style>
""", unsafe_allow_html=True)

# ASN Mapping
ASN_TO_PROVIDER = {
    16509: 'AWS', 14618: 'AWS', 19047: 'AWS', 8987: 'AWS',
    8075: 'Azure', 8068: 'Azure', 12076: 'Azure',
    15169: 'Google Cloud', 36040: 'Google Cloud', 19527: 'Google Cloud',
    13335: 'Cloudflare', 209242: 'Cloudflare',
    31898: 'Oracle Cloud', 20473: 'Oracle Cloud',
    36351: 'IBM Cloud', 12389: 'IBM Cloud',
    37963: 'Alibaba Cloud', 45102: 'Alibaba Cloud',
    14061: 'DigitalOcean', 393406: 'DigitalOcean',
    63949: 'Linode', 20473: 'Vultr',
    16276: 'OVH', 35540: 'OVH',
    24940: 'Hetzner',
    16625: 'Akamai', 20940: 'Akamai',
    54113: 'Fastly',
    27357: 'Rackspace', 33070: 'Rackspace',
}

def get_asn_from_ip(ip: str) -> Optional[tuple]:
    try:
        import dns.resolver
        parts = ip.split('.')
        reversed_ip = '.'.join(reversed(parts))
        query = f'{reversed_ip}.origin.asn.cymru.com'
        try:
            answers = dns.resolver.resolve(query, 'TXT')
            for rdata in answers:
                txt = str(rdata).strip('"')
                parts = [p.strip() for p in txt.split('|')]
                if len(parts) >= 1:
                    asn = int(parts[0])
                    try:
                        org_query = f'AS{asn}.asn.cymru.com'
                        org_answers = dns.resolver.resolve(org_query, 'TXT')
                        for org_rdata in org_answers:
                            org_txt = str(org_rdata).strip('"')
                            org_parts = [p.strip() for p in org_txt.split('|')]
                            if len(org_parts) >= 5:
                                org_name = org_parts[4]
                                return (asn, org_name)
                    except:
                        pass
                    return (asn, None)
        except:
            pass
    except:
        pass
    return None

def detect_cloud_provider_from_asn(asn: int, org_name: Optional[str]) -> tuple:
    if asn in ASN_TO_PROVIDER:
        return (ASN_TO_PROVIDER[asn], 'High')
    if org_name:
        org_lower = org_name.lower()
        if 'amazon' in org_lower or 'aws' in org_lower:
            return ('AWS', 'High')
        if 'microsoft' in org_lower or 'azure' in org_lower:
            return ('Azure', 'High')
        if 'google' in org_lower:
            return ('Google Cloud', 'Medium')
        if 'cloudflare' in org_lower:
            return ('Cloudflare', 'High')
        if any(word in org_lower for word in ['hosting', 'datacenter', 'server']):
            return (f'Hosting ({org_name})', 'Medium')
    return ('Other/Private', 'Low')

def check_autodiscover(domain: str) -> str:
    try:
        import dns.resolver
        try:
            answers = dns.resolver.resolve(f'autodiscover.{domain}', 'CNAME')
            for rdata in answers:
                target = str(rdata.target).lower()
                if any(ms in target for ms in ['outlook', 'office365', 'microsoft']):
                    return 'Microsoft 365'
        except:
            pass
        try:
            answers = dns.resolver.resolve(f'autodiscover.{domain}', 'A')
            return 'Microsoft 365'
        except:
            pass
    except:
        pass
    return None

def check_microsoft_records(domain: str) -> bool:
    try:
        import dns.resolver
        ms_subdomains = [f'autodiscover.{domain}', f'lyncdiscover.{domain}']
        for subdomain in ms_subdomains:
            try:
                dns.resolver.resolve(subdomain, 'A')
                return True
            except:
                pass
    except:
        pass
    return False

def detect_real_email_provider(domain: str, mx_string: str, spf_string: str) -> tuple:
    detections = []
    if spf_string:
        if any(ms in spf_string for ms in ['outlook.com', 'microsoft.com', 'office365', 'protection.outlook.com']):
            detections.append(('Microsoft 365', 'High', 'SPF'))
        if 'include:_spf.google.com' in spf_string or 'include:aspmx.googlemail.com' in spf_string:
            detections.append(('Google Workspace', 'High', 'SPF'))
    
    autodiscover_result = check_autodiscover(domain)
    if autodiscover_result:
        detections.append((autodiscover_result, 'High', 'Autodiscover'))
    
    if check_microsoft_records(domain):
        detections.append(('Microsoft 365', 'Medium', 'Microsoft DNS'))
    
    if not detections:
        return (None, 'Low', 'None')
    
    high_conf = [d for d in detections if d[1] == 'High']
    if len(high_conf) >= 1:
        ms_detections = [d for d in high_conf if 'Microsoft' in d[0]]
        if ms_detections:
            return ('Microsoft 365', 'Very High', high_conf[0][2])
        else:
            return (high_conf[0][0], 'Very High', high_conf[0][2])
    
    detections.sort(key=lambda x: {'Very High': 4, 'High': 3, 'Medium': 2, 'Low': 1}[x[1]], reverse=True)
    return detections[0]

def analyze_domain(domain: str) -> Dict[str, Any]:
    result = {
        'domain': domain,
        'main_ip': 'Unknown',
        'email_provider': 'Unknown',
        'cloud_provider': 'Unknown',
        'cdn_detected': 'No',
        'confidence': 'Low',
        'detection_method': 'None',
        'asn': 'Unknown',
        'notes': ''
    }
    
    try:
        result['main_ip'] = socket.gethostbyname(domain)
        ip = result['main_ip']
        
        asn_info = get_asn_from_ip(ip)
        if asn_info:
            asn_number, org_name = asn_info
            result['asn'] = f"AS{asn_number}"
            provider, confidence = detect_cloud_provider_from_asn(asn_number, org_name)
            result['cloud_provider'] = provider
            result['confidence'] = confidence
            
            if provider in ['Cloudflare', 'Akamai', 'Fastly']:
                result['cdn_detected'] = 'Yes'
            
            if org_name:
                result['notes'] = f'Org: {org_name}'
        else:
            if '104.21.' in ip or '172.64.' in ip:
                result['cloud_provider'] = 'Cloudflare'
                result['cdn_detected'] = 'Yes'
            elif ip.startswith(('52.', '54.', '3.')):
                result['cloud_provider'] = 'AWS'
            elif ip.startswith(('20.', '40.', '13.')):
                result['cloud_provider'] = 'Azure'
    except:
        result['notes'] = 'Domain not found'
    
    try:
        import dns.resolver
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_list = [str(r.exchange).lower() for r in mx_records]
        mx_string = ' '.join(mx_list)
        
        email_gateway = None
        if 'mimecast' in mx_string:
            email_gateway = 'Mimecast'
        elif 'proofpoint' in mx_string or 'pphosted' in mx_string:
            email_gateway = 'Proofpoint'
        elif 'barracuda' in mx_string:
            email_gateway = 'Barracuda'
        
        spf_string = ''
        try:
            txt_records = dns.resolver.resolve(domain, 'TXT')
            spf_records = [str(r).lower() for r in txt_records if 'spf' in str(r).lower()]
            spf_string = ' '.join(spf_records)
        except:
            pass
        
        if email_gateway:
            provider, conf, method = detect_real_email_provider(domain, mx_string, spf_string)
            if provider:
                result['email_provider'] = f"{provider} (via {email_gateway})"
                result['detection_method'] = method
            else:
                result['email_provider'] = f"{email_gateway} (provider unknown)"
        else:
            if 'aspmx.l.google.com' in mx_string or 'googlemail.com' in mx_string:
                result['email_provider'] = 'Google Workspace'
            elif 'outlook' in mx_string or 'microsoft' in mx_string or 'protection.outlook.com' in mx_string:
                result['email_provider'] = 'Microsoft 365'
            else:
                result['email_provider'] = mx_list[0] if mx_list else 'Unknown'
    except:
        pass
    
    return result

# Header
st.markdown("""
<div class="main-header">
    <h1>Cloud & Email Lookup Tool</h1>
    <p>Enterprise domain intelligence platform for infrastructure analysis</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["Analysis", "Results", "Export"])

with tab1:
    # How it works
    st.markdown("""
    <div class="how-it-works">
        <h3>How It Works</h3>
        <ol>
            <li><strong>Upload domains</strong> - Provide a list of company domains to analyze</li>
            <li><strong>Automatic analysis</strong> - System queries DNS records, ASN databases, and infrastructure data</li>
            <li><strong>Cloud detection</strong> - Identifies cloud providers (AWS, Azure, Google Cloud) via IP ownership analysis</li>
            <li><strong>Email detection</strong> - Determines email platforms (Microsoft 365, Google Workspace) through MX and SPF records</li>
            <li><strong>Security gateway detection</strong> - Identifies email security layers (Mimecast, Proofpoint)</li>
            <li><strong>Export results</strong> - Download comprehensive reports in CSV, Excel, or JSON format</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-title">Upload Domain List</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Select file (TXT or CSV format)",
            type=['txt', 'csv'],
            help="One domain per line (e.g., example.com)"
        )
    
    with col2:
        st.markdown('<div class="section-title">Paste Domains</div>', unsafe_allow_html=True)
        domains_text = st.text_area(
            "Enter domains (one per line)",
            height=150,
            placeholder="example.com\ncompany.com\ndomain.com"
        )
    
    domains = []
    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        domains = [line.strip() for line in content.split('\n') if line.strip()]
    elif domains_text:
        domains = [line.strip() for line in domains_text.split('\n') if line.strip()]
    
    if domains:
        st.success(f"{len(domains)} domains ready for analysis")
        
        if st.button("Start Analysis", use_container_width=True):
            with st.spinner('Analyzing domains...'):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results = []
                for i, domain in enumerate(domains):
                    status_text.text(f"Processing: {domain} ({i+1}/{len(domains)})")
                    progress_bar.progress((i + 1) / len(domains))
                    result = analyze_domain(domain)
                    results.append(result)
                
                st.session_state['results'] = results
                st.session_state['analyzed'] = True
                status_text.text("Analysis complete")
                st.success("Analysis completed successfully")
    else:
        st.info("Upload a file or paste domains to begin analysis")

with tab2:
    st.markdown('<div class="section-title">Analysis Results</div>', unsafe_allow_html=True)
    
    if 'analyzed' in st.session_state and st.session_state['analyzed']:
        results = st.session_state['results']
        
        total = len(results)
        cloud_count = {}
        email_count = {}
        cdn_count = 0
        high_conf = 0
        
        for r in results:
            cloud_count[r['cloud_provider']] = cloud_count.get(r['cloud_provider'], 0) + 1
            email_count[r['email_provider']] = email_count.get(r['email_provider'], 0) + 1
            if r['cdn_detected'] == 'Yes':
                cdn_count += 1
            if r['confidence'] == 'High':
                high_conf += 1
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total}</div>
                <div class="stat-label">Total Domains</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{high_conf}</div>
                <div class="stat-label">High Confidence</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{cdn_count}</div>
                <div class="stat-label">CDN Detected</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(cloud_count)}</div>
                <div class="stat-label">Cloud Providers</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Cloud Provider Distribution**")
            cloud_df = pd.DataFrame(list(cloud_count.items()), columns=['Provider', 'Count'])
            cloud_df = cloud_df.sort_values('Count', ascending=False)
            st.bar_chart(cloud_df.set_index('Provider'))
        
        with col2:
            st.markdown("**Email Provider Distribution**")
            email_df = pd.DataFrame(list(email_count.items()), columns=['Provider', 'Count'])
            email_df = email_df.sort_values('Count', ascending=False)
            st.bar_chart(email_df.set_index('Provider'))
        
        st.markdown("**Detailed Results**")
        
        col1, col2 = st.columns(2)
        with col1:
            cloud_filter = st.multiselect(
                "Filter by Cloud Provider",
                options=sorted(df['cloud_provider'].unique()) if 'df' in locals() else []
            )
        with col2:
            email_filter = st.multiselect(
                "Filter by Email Provider",
                options=sorted(df['email_provider'].unique()) if 'df' in locals() else []
            )
        
        df = pd.DataFrame(results)
        filtered_df = df.copy()
        if cloud_filter:
            filtered_df = filtered_df[filtered_df['cloud_provider'].isin(cloud_filter)]
        if email_filter:
            filtered_df = filtered_df[filtered_df['email_provider'].isin(email_filter)]
        
        st.dataframe(
            filtered_df[['domain', 'main_ip', 'cloud_provider', 'email_provider', 'cdn_detected', 'confidence']],
            use_container_width=True,
            height=400
        )
        
    else:
        st.info("Complete analysis to view results")

with tab3:
    st.markdown('<div class="section-title">Export Results</div>', unsafe_allow_html=True)
    
    if 'analyzed' in st.session_state and st.session_state['analyzed']:
        results = st.session_state['results']
        
        st.markdown("**Available Export Formats**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_buffer = io.StringIO()
            df = pd.DataFrame(results)
            df.to_csv(csv_buffer, index=False)
            
            st.download_button(
                label="Download CSV",
                data=csv_buffer.getvalue(),
                file_name=f"domain_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            
            st.download_button(
                label="Download Excel",
                data=excel_buffer.getvalue(),
                file_name=f"domain_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col3:
            json_str = pd.DataFrame(results).to_json(orient='records', indent=2)
            
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"domain_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.success("Export formats ready for download")
        
    else:
        st.info("Complete analysis to export results")
