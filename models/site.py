from sql_alchemy import banco

class SiteModel(banco.Model):
    __tablename__ = 'sites'

    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel') # lista de objetos hoteis

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis]
        }
    
    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site
        return None
    
    def save_site(slef):
        banco.session.add(slef)
        banco.session.commit()

    def update_site(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
    
    def delete_site(self):
        banco.session.delete(self)
        banco.session.commit()