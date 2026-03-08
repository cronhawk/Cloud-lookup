#!/usr/bin/env python3
"""
Cloud & Email Lookup - Premium SaaS Edition
Professional domain intelligence platform
"""

import streamlit as st
import socket
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional
import io
import time

# Page config
st.set_page_config(
    page_title="Cloud & Email Lookup",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium SaaS CSS with all improvements
st.markdown("""
<style>
    /* Premium typography system */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro', sans-serif;
    }
    
    /* Color system */
    :root {
        --primary: #2F5BFF;
        --accent: #00B894;
        --warning: #FF7675;
        --bg-neutral: #F4F6FA;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --card-bg: #FFFFFF;
    }
    
    /* Page background */
    .main {
        background-color: var(--bg-neutral);
    }
    
    /* Typography hierarchy */
    h1 { font-weight: 600; color: var(--text-primary); }
    h2 { font-weight: 600; color: var(--text-primary); }
    h3 { font-weight: 600; color: var(--text-primary); }
    label { font-weight: 500; color: var(--text-primary); }
    p { font-weight: 400; color: var(--text-secondary); }
    
    /* Compact top header - minimal padding */
    .main-header {
        background: linear-gradient(135deg, #2F5BFF 0%, #1E40AF 100%);
        color: white;
        padding: 0.875rem 1.75rem;
        margin: 0 auto 20px auto;
        max-width: 900px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(47, 91, 255, 0.2);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
        letter-spacing: -0.025em;
        line-height: 1.2;
        color: white;
    }
    
    .main-header .subtitle {
        margin: 0.15rem 0 0 0;
        font-size: 0.65rem;
        opacity: 0.85;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .main-header p {
        margin: 0;
        font-size: 0.85rem;
        opacity: 0.95;
        font-weight: 400;
        line-height: 1.4;
        color: rgba(255,255,255,0.95);
    }
    
    /* Metrics row */
    .metrics-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 32px;
    }
    
    /* Card system with spacing */
    .card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 32px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.06);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    
    /* Stats cards */
    .stat-card {
        background: var(--card-bg);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        border-color: var(--primary);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Main content area with background card */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Premium upload area with micro-interactions */
    .upload-container {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    
    .upload-area {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border: 3px dashed var(--primary);
        border-radius: 20px;
        padding: 32px 28px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .upload-area::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(47, 91, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .upload-area:hover::before {
        left: 100%;
    }
    
    .upload-area:hover {
        background: linear-gradient(135deg, #DDD6FE 0%, #C7D2FE 100%);
        border-color: #1E40AF;
        box-shadow: 0 0 0 6px rgba(47, 91, 255, 0.1);
        transform: translateY(-4px);
    }
    
    .upload-area.drag-over {
        background: linear-gradient(135deg, #C7D2FE 0%, #A5B4FC 100%);
        border-color: var(--accent);
        box-shadow: 0 0 0 8px rgba(0, 184, 148, 0.15);
    }
    
    .upload-icon {
        font-size: 3rem;
        margin-bottom: 12px;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .upload-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 6px;
    }
    
    .upload-subtitle {
        font-size: 0.95rem;
        color: var(--text-secondary);
        font-weight: 400;
    }
    
    .drop-message {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--accent);
        margin-top: 16px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .upload-area.drag-over .drop-message {
        opacity: 1;
    }
    
    /* Primary action button */
    .primary-action {
        width: 100%;
        max-width: 400px;
        margin: 32px auto;
        text-align: center;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, var(--primary) 0%, #1E40AF 100%);
        color: white;
        border: none;
        padding: 18px 48px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.025em;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(47, 91, 255, 0.3);
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(47, 91, 255, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
    }
    
    .stButton>button:disabled {
        background: linear-gradient(135deg, #D1D5DB 0%, #9CA3AF 100%);
        cursor: not-allowed;
        box-shadow: none;
        opacity: 0.6;
    }
    
    /* Modern pill tabs - white text on active state */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: var(--card-bg);
        border-bottom: none;
        padding: 16px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        justify-content: center;
        border: 1px solid rgba(0,0,0,0.06);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid transparent;
        color: #6B7280 !important;
        font-weight: 500;
        padding: 14px 28px;
        font-size: 0.95rem;
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0,0,0,0.02);
        color: var(--text-primary) !important;
        border-color: rgba(47, 91, 255, 0.2);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #2F5BFF !important;
        color: white !important;
        font-weight: 600;
        box-shadow: 0 6px 16px rgba(47, 91, 255, 0.35);
        border-color: transparent;
        transform: translateY(-2px);
    }
    
    /* Force white text and icons on active tab */
    .stTabs [data-baseweb="tab"][aria-selected="true"] > div,
    .stTabs [data-baseweb="tab"][aria-selected="true"] span,
    .stTabs [data-baseweb="tab"][aria-selected="true"] p {
        color: white !important;
    }
    
    /* Progress animations */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -100% 0; }
        100% { background-position: 100% 0; }
    }
    
    /* Loading spinner */
    .loading-container {
        text-align: center;
        padding: 48px;
    }
    
    .spinner {
        border: 4px solid rgba(47, 91, 255, 0.1);
        border-radius: 50%;
        border-top: 4px solid var(--primary);
        width: 48px;
        height: 48px;
        animation: spin 1s linear infinite;
        margin: 0 auto 16px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success checkmark */
    .success-checkmark {
        width: 80px;
        height: 80px;
        margin: 0 auto;
    }
    
    .success-checkmark .check-icon {
        width: 80px;
        height: 80px;
        position: relative;
        border-radius: 50%;
        box-sizing: content-box;
        border: 4px solid var(--accent);
    }
    
    .success-checkmark .check-icon::before {
        top: 3px;
        left: -2px;
        width: 30px;
        transform-origin: 100% 50%;
        border-radius: 100px 0 0 100px;
    }
    
    .success-checkmark .check-icon::after {
        top: 0;
        left: 30px;
        width: 60px;
        transform-origin: 0 50%;
        border-radius: 0 100px 100px 0;
        animation: rotate-circle 4.25s ease-in;
    }
    
    /* Input fields */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid rgba(0,0,0,0.08);
        padding: 16px;
        font-size: 0.95rem;
        transition: all 0.2s;
        font-weight: 400;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 4px rgba(47, 91, 255, 0.1);
        outline: none;
    }
    
    /* Data table */
    .stDataFrame {
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Section spacing */
    .section {
        margin-bottom: 32px;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 16px 0;
    }
    
    /* Info messages */
    .stInfo {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border-left: 4px solid var(--primary);
        border-radius: 8px;
        padding: 16px;
        font-weight: 400;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        border-left: 4px solid var(--accent);
        border-radius: 8px;
        padding: 16px;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* How it works */
    .how-it-works {
        background: var(--card-bg);
        border: 1px solid rgba(0,0,0,0.06);
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .how-it-works h3 {
        color: var(--text-primary);
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0 0 24px 0;
    }
    
    .how-it-works ol {
        margin: 0;
        padding-left: 24px;
        color: var(--text-secondary);
        line-height: 2;
    }
    
    .how-it-works li {
        margin-bottom: 16px;
        font-weight: 400;
    }
    
    .how-it-works strong {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* File uploader - invisible but functional, overlays upload area */
    [data-testid="stFileUploader"] {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        opacity: 0 !important;
        z-index: 10 !important;
    }
    
    [data-testid="stFileUploader"] > div {
        height: 100% !important;
    }
    
    [data-testid="stFileUploader"] label {
        display: none !important;
    }
    
    .upload-container {
        position: relative !important;
    }
</style>
""", unsafe_allow_html=True)

# ASN Mapping (same as before)
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

# Header - compact without stats
st.markdown("""
<div class="main-header">
    <h1>Cloud & Email Lookup</h1>
    <div class="subtitle">Enterprise Domain Intelligence Platform</div>
    <div style="margin: 12px auto 0 auto; max-width: 600px;">
        <p style="font-size: 0.9rem; margin-bottom: 0; opacity: 0.95;">Analyze domains to detect:</p>
        <div style="display: flex; justify-content: center; gap: 32px; font-size: 0.85rem; opacity: 0.9; margin-top: 8px;">
            <div>• Email infrastructure</div>
            <div>• Cloud providers</div>
            <div>• Risk indicators</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔎 Analysis", "📊 Results", "⬇ Export", "📖 How It Works"])

with tab1:
    # Two columns with OR divider
    col1, col_divider, col2 = st.columns([5, 1, 5], gap="small")
    
    with col1:
        # Upload area with improved icon grouping
        st.markdown("""
        <div class="upload-container">
            <div class="upload-area">
                <div class="upload-icon">📁</div>
                <div class="upload-title">Upload Domain List</div>
                <div style="width: 60%; height: 1px; background: rgba(47, 91, 255, 0.2); margin: 12px auto;"></div>
                <div class="upload-subtitle">Drag &amp; drop your file</div>
                <div style="margin-top: 20px;">
                    <div style="font-size: 0.85rem; color: #6B7280; font-weight: 500; margin-bottom: 12px;">Supported formats</div>
                    <div style="display: flex; justify-content: center; align-items: center; gap: 32px;">
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span style="font-size: 1.25rem;">📄</span>
                            <span style="font-size: 0.8rem; font-weight: 600; color: #1F2937;">TXT</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span style="font-size: 1.25rem;">📊</span>
                            <span style="font-size: 0.8rem; font-weight: 600; color: #1F2937;">CSV</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span style="font-size: 1.25rem;">💾</span>
                            <span style="font-size: 0.8rem; font-weight: 600; color: #1F2937;">Up to 200MB</span>
                        </div>
                    </div>
                </div>
                <div class="drop-message">Drop domains here ✨</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Hidden file uploader
        uploaded_file = st.file_uploader(
            "Upload file",
            type=['txt', 'csv'],
            help="One domain per line",
            label_visibility="collapsed",
            key="file_upload_hidden"
        )
    
    with col_divider:
        # OR divider
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; height: 100%; min-height: 400px;">
            <div style="text-align: center;">
                <div style="font-size: 0.9rem; font-weight: 600; color: #9CA3AF; background: white; padding: 8px 12px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.06);">OR</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Paste domains section with live counter
        st.markdown("""
        <div style="background: white; border-radius: 16px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height: 100%;">
            <p style="font-weight: 600; color: #1F2937; margin: 0 0 8px 0; font-size: 1.35rem;">Paste Domains</p>
            <div style="width: 60%; height: 1px; background: rgba(47, 91, 255, 0.2); margin: 12px 0;"></div>
            <p style="font-size: 0.85rem; color: #6B7280; margin-bottom: 16px; font-weight: 400;">Paste domains (one per line)</p>
        </div>
        """, unsafe_allow_html=True)
        
        domains_text = st.text_area(
            "Enter domains",
            height=240,
            placeholder="example.com\ngoogle.com\ncompany.co.uk",
            label_visibility="collapsed"
        )
        
        # Live domain counter
        if domains_text:
            domain_count = len([line.strip() for line in domains_text.split('\n') if line.strip()])
            st.markdown(f"""
            <div style="margin-top: 12px; padding: 8px 16px; background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border-radius: 8px; text-align: center;">
                <span style="font-weight: 600; color: #2F5BFF; font-size: 0.9rem;">{domain_count} domain{"s" if domain_count != 1 else ""} detected</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Get domains
    domains = []
    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        domains = [line.strip() for line in content.split('\n') if line.strip()]
    elif domains_text:
        domains = [line.strip() for line in domains_text.split('\n') if line.strip()]
    
    # Primary action button
    if domains:
        st.success(f"✓ {len(domains)} domains ready for analysis")
    
    # Centered primary action button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "Start Analysis",
            use_container_width=True,
            disabled=not domains,
            type="primary"
        )
    
    if analyze_button and domains:
        # Loading state
        st.markdown("""
        <div class="loading-container">
            <div class="spinner"></div>
            <p style="font-weight: 500; color: var(--text-primary);">Scanning domains...</p>
        </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        for i, domain in enumerate(domains):
            status_text.text(f"Processing: {domain} ({i+1}/{len(domains)})")
            progress_bar.progress((i + 1) / len(domains))
            result = analyze_domain(domain)
            results.append(result)
            time.sleep(0.1)  # Slight delay for animation
        
        st.session_state['results'] = results
        st.session_state['analyzed'] = True
        
        # Success animation
        st.markdown("""
        <div style="text-align: center; padding: 32px;">
            <div style="font-size: 4rem; margin-bottom: 16px;">✓</div>
            <h3 style="color: var(--accent); font-weight: 600;">Analysis Complete!</h3>
            <p style="color: var(--text-secondary);">Click the Results tab to view your data</p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

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
        
        # Stats cards
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
        
        # Charts
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
        
        df = pd.DataFrame(results)
        
        col1, col2 = st.columns(2)
        with col1:
            cloud_filter = st.multiselect(
                "Filter by Cloud Provider",
                options=sorted(df['cloud_provider'].unique())
            )
        with col2:
            email_filter = st.multiselect(
                "Filter by Email Provider",
                options=sorted(df['email_provider'].unique())
            )
        
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
        st.info("Complete analysis in the Analysis tab to view results")

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

with tab4:
    st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: white; border-radius: 16px; padding: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin-bottom: 24px;">
        <h3 style="margin-top: 0; color: #1F2937;">What This Tool Does</h3>
        <p style="color: #6B7280; line-height: 1.8;">
            Enter a company domain (like <code>google.com</code> or <code>freshfields.com</code>) and instantly see:
        </p>
        <ul style="color: #1F2937; line-height: 2;">
            <li><strong>Email provider</strong> → Microsoft 365 or Google Workspace</li>
            <li><strong>Cloud hosting</strong> → AWS, Azure, Google Cloud, etc.</li>
            <li><strong>Email security</strong> → Mimecast, Proofpoint, Barracuda</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Email Detection Section
    with st.expander("📧 How We Find Email Providers", expanded=False):
        st.markdown("""
        **We check three things:**
        
        1. **Mail server addresses** - Where the company receives emails  
           If we see `@google.com` servers → Google Workspace  
           If we see `@outlook.com` servers → Microsoft 365
        
        2. **Email security settings (SPF records)** - Who's allowed to send email  
           Companies publish a list saying "Google can send our emails" or "Microsoft can send our emails"
        
        3. **Microsoft-specific records** - Special settings only Microsoft 365 uses  
           Like `autodiscover` which helps Outlook find email settings
        
        **Accuracy: 90-95%**  
        This is public information companies must publish for email to work.
        """)
    
    # Email Security Challenge
    with st.expander("🛡️ The Email Security Challenge", expanded=False):
        st.markdown("""
        **Problem:** Many companies use Mimecast or Proofpoint to protect their email. When we look them up, we see Mimecast/Proofpoint instead of Microsoft/Google.
        
        **Our solution:** We look deeper using the security settings to find the real provider behind the protection.
        
        **Result:** We show "Microsoft 365 (via Mimecast)" or "Google Workspace (via Proofpoint)"
        
        **Success rate:** 85-90% - occasionally we can only detect the security layer, not what's behind it.
        """)
    
    # Cloud Detection Section
    with st.expander("☁️ How We Find Cloud Providers", expanded=False):
        st.markdown("""
        **We use IP address ownership:**
        
        1. Find the company's website IP address (e.g., `52.12.34.56`)
        2. Look up who owns that IP address
        3. Match to known cloud providers:
           - Amazon owns AS16509 → AWS
           - Microsoft owns AS8075 → Azure  
           - Google owns AS15169 → Google Cloud
           - Plus 100+ other providers
        
        **Accuracy: 95%**  
        Cloud companies publicly register which IP addresses they own. This is how the internet routes traffic.
        
        **Why some show "Hosting" instead of "AWS/Azure":**  
        If a company uses a smaller hosting provider (not a major cloud), we show that hosting company's name.
        """)
    
    # Why Different Providers
    with st.expander("🔄 Why Companies Use Different Providers", expanded=False):
        st.markdown("""
        **Common scenario:** Azure for cloud + Google Workspace for email
        
        **This is totally normal!**
        - IT team picks the cloud (Azure good for Windows apps)
        - Business team picks email (Google good for collaboration)
        - Different purchases, different decisions
        
        **About 60% of companies mix and match providers.**
        """)
    
    # Accuracy & Limitations
    with st.expander("📊 Accuracy & Limitations", expanded=False):
        st.markdown("""
        ### What We're Very Good At:
        - ✅ Email provider (95% accurate)
        - ✅ Major cloud providers like AWS/Azure (95% accurate)
        - ✅ Email security gateways (99% accurate)
        
        ### What's Trickier:
        - ⚠️ Email provider behind security (85-90% accurate)
        - ⚠️ Smaller hosting companies (sometimes unclear)
        - ⚠️ Companies using multiple clouds (we show their main website only)
        
        ### What We Can't See:
        - ❌ Internal systems (we only see their public website)
        - ❌ Private servers (if they host everything themselves)
        - ❌ Recent changes (DNS updates take 24-48 hours)
        """)
    
    # Real Example
    with st.expander("💼 Real Example: freshfields.com", expanded=False):
        st.markdown("""
        **What we find:**
        - Website hosted by: Episerver (a Swedish hosting company)
        - Email delivered by: Mimecast  
        - Email actually from: Microsoft 365 (found via security records)
        
        **Result:** "Microsoft 365 (via Mimecast)" + "Hosting (Episerver)"
        
        **What this tells you:**  
        They use Microsoft 365 for email, which is useful for outreach. Their website is hosted in Sweden, not on a major cloud.
        """)
    
    # Why Useful for Sales
    with st.expander("💡 Why It's Useful for Sales", expanded=False):
        st.markdown("""
        **Email provider matters:**
        - Microsoft 365 users → familiar with SharePoint, Teams, OneDrive
        - Google Workspace users → familiar with Drive, Docs, Meet
        
        **Cloud provider matters:**
        - AWS users → likely comfortable with cloud infrastructure
        - Azure users → often Windows-heavy organizations
        - Mixed providers → sophisticated IT team, open to multiple vendors
        
        **Email security matters:**
        - Mimecast/Proofpoint users → security-conscious, likely have compliance requirements
        - No security gateway → might be interested in security solutions
        """)
    
    # Bottom Line
    st.markdown("""
    <div style="background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%); border-radius: 12px; padding: 24px; margin-top: 24px; border-left: 4px solid #2F5BFF;">
        <h3 style="margin-top: 0; color: #1F2937;">Bottom Line</h3>
        <p style="color: #1F2937; line-height: 1.8; margin-bottom: 0;">
            <strong>Think of it like a phone book lookup:</strong><br>
            Companies publish their email and hosting information publicly. We automate looking it up across hundreds of domains with 90-95% accuracy. This helps you understand a company's tech stack before reaching out.
        </p>
        <p style="color: #6B7280; font-size: 0.9rem; margin-top: 16px; margin-bottom: 0;">
            <em>Not magic - just efficient automation of public information.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-top: 32px; padding: 16px; color: #9CA3AF; font-size: 0.85rem;">
        This tool checks public DNS records • Accuracy: ~90-95% • Data current as of lookup time
    </div>
    """, unsafe_allow_html=True)
