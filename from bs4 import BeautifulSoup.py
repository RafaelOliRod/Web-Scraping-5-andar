rom bs4 import BeautifulSoup

html = '''
<div class="sc-740uoz-0 gnxvcs">
  <div data-testid="house-card-container-rent" width="100%" class="sc-1uhd8i-1 bTndEd">
    <a target="_blank" title="Apartamento para alugar com 2 quartos, 67m² em Tijuca, Rio de Janeiro" class="sc-1d0oyoa-0 bfDoiv" href="https://www.quintoandar.com.br/imovel/894495301/alugar/apartamento-2-quartos-tijuca-rio-de-janeiro?from_route=%22search_results%22&amp;house_tags=exclusivity&amp;house_tags=newAd&amp;search_id=%22d6093423-023a-431a-8155-65e9b8e8fec3%22&amp;search_rank=%7B%22sortMode%22%3A%22relevance%22%2C%22searchMode%22%3A%22list%22%2C%22resultsOrigin%22%3A%22search%22%2C%22rank%22%3A0%2C%22personalization%22%3Afalse%7D">
      <div class="sc-hTtwUo iTcdQ Cozy__FindHouseCard-Container" role="group" tabindex="0" aria-label="Apartamento . Exclusivo, Anúncio novo. Tijuca, Rio de Janeiro, Rua Barão de Pirassinunga. 67 metros quadrados, 2 quartos de garagem.  R$ 2.200 aluguel, R$ 2.613 total.">
        <div class="Cozy__CardBlock-Container _2pfuCF znH6Fs qf-bDA" role="button" tabindex="0" aria-live="polite">
          <div class="Cozy__CardRow-Container oVdjIf" style="--card-row-top:0;--card-row-bottom:0;--card-row-left:0;--card-row-right:0;--card-row-space-between:0" role="complementary">
            <div class="Cozy__CardMedia-Wrapper Cozy__CardMedia--with-indicator-bullet Cozy__CardMedia--with-navigation-on-hover Cozy__CardMedia--with-tag Cozy__CardMedia--with-aspect-ratio-3:2 XdJlXC">
              <div class="Cozy__CardMedia-CarouselSection sGDxzt">
                <div class="Cozy__CardMedia-TagSection RUm0w-" role="presentation" aria-hidden="true">
                  <span class="Cozy__Tag Cozy__Tag-Wrapper XSKuMT MJVZE7"><span class="CozyTypography Cozy__Tag-Label xih2fc EKXjIf pwAPLE">Exclusivo</span></span>
                  <span class="Cozy__Tag Cozy__Tag-Wrapper XSKuMT MJVZE7"><span class="CozyTypography Cozy__Tag-Label xih2fc EKXjIf pwAPLE">Anúncio novo</span></span>
                </div>
                <div class="_5GOKEz" style="--aspect-ratio:1.5">
                  <div class="Cozy__CarouselCore TD1gQ6 N8CtsJ">
                    <div class="swiper">
                      <div class="swiper-wrapper">
                        <div class="swiper-slide">
                          <div class="Cozy__ImageCarouselItem-Wrapper HJY4vG" id="0" role="img" tabindex="-1" aria-label="Foto 1 de 12" aria-hidden="true">
                            <div class="sc-1h0uppf-0 fSWNSS">
                              <img alt="Sala de apartamento para alugar com 2 quartos, 67m² em Tijuca, Rio de Janeiro" loading="lazy" fetchPriority="low" src="/img/med/894495301-691.1759477988941MVF0427.JPG" srcSet="/img/xsm/894495301-691.1759477988941MVF0427.JPG 120w,/img/sml/894495301-691.1759477988941MVF0427.JPG">
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </a>
  </div>
</div>
'''

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Find the link
link = soup.find('a')['href']

print(link)
