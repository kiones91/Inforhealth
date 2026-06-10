"""Snippet CTA final + footer premium (padrão index.html)."""

SOCIAL_LINKS = {
    "instagram": "https://www.instagram.com/inforhealth_edu",
    "linkedin": "https://www.linkedin.com/company/inforhealth-educacao-excelencia-saude",
    "facebook": "https://www.facebook.com/inforhealth",
    "youtube": "https://www.youtube.com/@inforhealth_edu",
    "whatsapp": "https://wa.me/5519997773084",
    "maps": "https://www.google.com/maps/search/Inforhealth+Educação+Campinas",
}


def footer_social_html() -> str:
    return f"""        <div class="site-footer-social reveal" aria-label="Redes sociais Inforhealth">
          <a href="{SOCIAL_LINKS['instagram']}" target="_blank" rel="noopener noreferrer" aria-label="Instagram Inforhealth">
            <iconify-icon icon="mdi:instagram" width="20"></iconify-icon>
          </a>
          <a href="{SOCIAL_LINKS['linkedin']}" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn Inforhealth">
            <iconify-icon icon="mdi:linkedin" width="20"></iconify-icon>
          </a>
          <a href="{SOCIAL_LINKS['facebook']}" target="_blank" rel="noopener noreferrer" aria-label="Facebook Inforhealth">
            <iconify-icon icon="mdi:facebook" width="20"></iconify-icon>
          </a>
          <a href="{SOCIAL_LINKS['youtube']}" target="_blank" rel="noopener noreferrer" aria-label="YouTube Inforhealth">
            <iconify-icon icon="mdi:youtube" width="20"></iconify-icon>
          </a>
          <a href="{SOCIAL_LINKS['whatsapp']}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp Inforhealth">
            <iconify-icon icon="mdi:whatsapp" width="20"></iconify-icon>
          </a>
          <a href="{SOCIAL_LINKS['maps']}" target="_blank" rel="noopener noreferrer" aria-label="Google Maps Inforhealth Campinas">
            <iconify-icon icon="mdi:google-maps" width="20"></iconify-icon>
          </a>
        </div>"""


def closing_zone_footer(asset_prefix=""):
    """asset_prefix: '' para raiz do esqueleto, '../../' para blog/artigos/."""
    p = asset_prefix
    img = f"{p}../assets/imagens/institucional/logo-inforhealth-2020.webp"
    return f"""<!-- CTA + FOOTER -->
<section id="cta-final" class="closing-zone px-8 lg:px-16 xl:px-24 pb-0">
  <div class="cta-final-card reveal border-gradient">
    <div class="cta-final-grid-bg" aria-hidden="true"></div>
    <div class="cta-final-glow cta-final-glow--left" aria-hidden="true"></div>
    <div class="cta-final-glow cta-final-glow--right" aria-hidden="true"></div>
    <div class="beam-h top-1/3 w-full opacity-30" style="animation-delay:1.5s;"></div>
    <div class="cta-final-inner">
      <div class="cta-final-copy">
        <div class="cta-final-label-wrap">
          <span class="cta-final-label-dot" aria-hidden="true"></span>
          <span class="cta-final-label">Atendimento humano</span>
        </div>
        <h2 class="cta-final-title">Ficou com dúvida?<br/><span class="cta-final-title-accent">A gente te orienta agora.</span></h2>
        <p class="cta-final-desc">Cursos, eventos, In Company ou trilhas corporativas — fale com quem entende do mercado de saúde. <strong>Sem robô, sem fila.</strong></p>
        <div class="cta-final-trust">
          <span class="cta-final-trust-item"><iconify-icon icon="solar:clock-circle-linear" width="16"></iconify-icon> Resposta em minutos</span>
          <span class="cta-final-trust-item"><iconify-icon icon="solar:calendar-linear" width="16"></iconify-icon> Seg a Sex · 9h–18h</span>
          <span class="cta-final-trust-item"><iconify-icon icon="solar:verified-check-linear" width="16"></iconify-icon> 190+ empresas</span>
        </div>
      </div>
      <div class="cta-final-panel">
        <div class="cta-final-panel-head">
          <div class="cta-final-avatar" aria-hidden="true">
            <iconify-icon icon="solar:chat-round-dots-bold" width="28"></iconify-icon>
            <span class="cta-final-avatar-pulse"></span>
          </div>
          <div>
            <p class="cta-final-panel-title">Time comercial Inforhealth</p>
            <p class="cta-final-panel-sub">Online agora · Campinas/SP</p>
          </div>
        </div>
        <a href="https://wa.me/5519997773084" class="btn-glass btn-glass-accent btn-glass-lg cta-final-btn-primary">
          <iconify-icon icon="solar:chat-round-dots-linear" width="18"></iconify-icon> Falar no WhatsApp
        </a>
        <a href="{p}cursos.html" class="btn-glass btn-glass-light btn-glass-md cta-final-btn-secondary">
          Ver turmas abertas <iconify-icon icon="solar:arrow-right-linear" width="16"></iconify-icon>
        </a>
        <a href="tel:+5519997773084" class="cta-final-phone">
          <iconify-icon icon="solar:phone-linear" width="14"></iconify-icon> +55 19 99777-3084
        </a>
      </div>
    </div>
  </div>
</section>

<footer class="site-footer">
  <div class="site-footer-glow" aria-hidden="true"></div>
  <div class="site-footer-inner px-8 lg:px-16 xl:px-24">
    <div class="site-footer-top">
      <div class="site-footer-brand reveal">
        <img src="{img}" alt="Inforhealth Educação" class="site-footer-logo" width="160" height="36"/>
        <p class="site-footer-tagline">Excelência em capacitação para profissionais e instituições de saúde em todo o Brasil.</p>
        <div class="site-footer-stats">
          <div class="site-footer-stat">
            <strong>190+</strong>
            <span>Empresas</span>
          </div>
          <div class="site-footer-stat">
            <strong>6k+</strong>
            <span>Alunos</span>
          </div>
          <div class="site-footer-stat">
            <strong>36+</strong>
            <span>Cursos</span>
          </div>
        </div>
      </div>
      <div class="site-footer-nav">
        <div class="site-footer-col reveal footer-reveal-delay-1">
          <h3 class="site-footer-heading">Formação</h3>
          <ul class="site-footer-links">
            <li><a href="{p}cursos.html"><iconify-icon icon="solar:book-bookmark-linear" width="15"></iconify-icon> Cursos</a></li>
            <li><a href="{p}eventos.html"><iconify-icon icon="solar:calendar-linear" width="15"></iconify-icon> Eventos</a></li>
            <li><a href="{p}in-company.html"><iconify-icon icon="solar:buildings-2-linear" width="15"></iconify-icon> In Company</a></li>
            <li><a href="{p}academia-360.html"><iconify-icon icon="solar:graph-up-linear" width="15"></iconify-icon> Academia 360</a></li>
          </ul>
        </div>
        <div class="site-footer-col reveal footer-reveal-delay-2">
          <h3 class="site-footer-heading">Institucional</h3>
          <ul class="site-footer-links">
            <li><a href="{p}sobre.html"><iconify-icon icon="solar:info-circle-linear" width="15"></iconify-icon> Sobre</a></li>
            <li><a href="{p}equipe.html"><iconify-icon icon="solar:users-group-rounded-linear" width="15"></iconify-icon> Equipe</a></li>
            <li><a href="{p}blog.html"><iconify-icon icon="solar:document-text-linear" width="15"></iconify-icon> Blog</a></li>
            <li><a href="{p}contato.html"><iconify-icon icon="solar:letter-linear" width="15"></iconify-icon> Contato</a></li>
          </ul>
        </div>
        <div class="site-footer-col reveal footer-reveal-delay-3">
          <h3 class="site-footer-heading">Contato</h3>
          <ul class="site-footer-links">
            <li><a href="mailto:contato@inforhealth.com.br"><iconify-icon icon="solar:letter-linear" width="15"></iconify-icon> contato@inforhealth.com.br</a></li>
            <li><a href="https://wa.me/5519997773084"><iconify-icon icon="solar:chat-round-dots-linear" width="15"></iconify-icon> WhatsApp</a></li>
            <li><a href="{p}ebook.html"><iconify-icon icon="solar:download-linear" width="15"></iconify-icon> E-book gratuito</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="site-footer-bottom reveal footer-reveal-delay-4">
{footer_social_html()}
      <p>© 2026 Inforhealth Educação e Excelência em Saúde</p>
      <p class="site-footer-bottom-note">Capacitação estratégica em gestão, qualidade e compliance · Campinas/SP</p>
    </div>
  </div>
</footer>"""
