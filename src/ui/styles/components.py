"""
Components CSS module: Premium quote box and custom components
"""

def load_components_css():
    return """
    /* Premium Quote Box */
    .rr-quote-wrap {
      margin: 32px 0 10px 0;
      padding: 34px 40px;
      border-radius: 22px;
      background: linear-gradient(135deg, #2B66F6 0%, #1E3A8A 100%);
      position: relative;
      overflow: hidden;
      box-shadow: 0 14px 36px rgba(2, 6, 23, 0.18);
    }
    .rr-quote-wrap:hover {
      transform: translateY(-2px);
      transition: 160ms ease;
    }
    .rr-quote-wrap:before {
      content: "";
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.18), transparent 40%),
                  radial-gradient(circle at 85% 25%, rgba(255,255,255,0.10), transparent 35%);
      pointer-events: none;
    }
    .rr-quote {
      font-size: 22px;
      line-height: 1.45;
      font-weight: 650;
      color: rgba(255,255,255,0.92) !important;
      margin: 0;
      letter-spacing: -0.2px;
      font-family: 'Inter', sans-serif !important;
      position: relative;
      z-index: 2;
    }
    .rr-quote-mark {
      position: absolute;
      top: 18px;
      left: 18px;
      font-size: 52px;
      color: rgba(255,255,255,0.28);
      font-weight: 900;
      z-index: 1;
    }
    .rr-quote-sub {
      margin-top: 14px;
      color: rgba(255,255,255,0.72) !important;
      font-size: 13px;
      letter-spacing: 0.2px;
      position: relative;
      z-index: 2;
    }
    .rr-quote-sub span {
      display: inline-block;
      padding: 6px 10px;
      border: 1px solid rgba(255,255,255,0.22);
      border-radius: 999px;
      background: rgba(15, 23, 42, 0.18);
      color: rgba(255,255,255,0.9) !important;
    }
    .rr-center {
      max-width: 980px;
      margin: 0 auto;
    }
"""
