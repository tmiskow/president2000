import os
import pandas as pd
from jinja2 import Environment, FileSystemLoader

full_data = pd.read_csv('pkw2000.csv')
environment = Environment(loader=FileSystemLoader('templates'))

voivodeships_codes = {
    'Dolnośląskie': 'PL-DS',
    'Kujawsko-Pomorskie': 'PL-KP',
    'Lubelskie': 'PL-LU',
    'Lubuskie': 'PL-LB',
    'Mazowieckie': 'PL-MZ',
    'Małopolskie': 'PL-MA',
    'Opolskie': 'PL-OP',
    'Podkarpackie': 'PL-PK',
    'Podlaskie': 'PL-PD',
    'Pomorskie': 'PL-PM',
    'Warmińsko-Mazurskie': 'PL-WN',
    'Wielkopolskie': 'PL-WP',
    'Zachodniopomorskie': 'PL-ZP',
    'Łódzkie': 'PL-LD',
    'Śląskie': 'PL-SL',
    'Świętokrzyskie': 'PL-SK'
}

candidates = list(full_data.columns.difference([
    'Głosy ważne', 'Głosy oddane', 'Głosy nieważne', 'Uprawnieni', 'Karty wydane',
    'Nr okręgu', 'Kod gminy', 'Gmina', 'Powiat', 'Województwo', 'Obwody'
]))

candidates_images = {
    'Aleksander KWAŚNIEWSKI': 'kwasniewski.jpg',
    'Andrzej LEPPER': 'lepper.jpg',
    'Andrzej Marian OLECHOWSKI': 'olechowski.jpg',
    'Bogdan PAWŁOWSKI': 'pawlowski.jpg',
    'Dariusz Maciej GRABOWSKI': 'grabowski.jpg',
    'Jan ŁOPUSZAŃSKI': 'lopuszanski.jpg',
    'Janusz KORWIN-MIKKE': 'korwin-mikke.jpg',
    'Jarosław KALINOWSKI': 'kalinowski.jpg',
    'Lech WAŁĘSA': 'walesa.jpg',
    'Marian KRZAKLEWSKI': 'krzaklewski.jpg',
    'Piotr IKONOWICZ': 'ikonowicz.jpg',
    'Tadeusz Adam WILECKI': 'wilecki.jpg'
}


def generate_country_template(data):
    filename = 'index.html'

    allowed = data['Uprawnieni'].sum()
    all_votes = data['Głosy oddane'].sum()
    turnout = all_votes / allowed

    results = data[candidates].sum().to_frame('votes')
    valid_votes = data['Głosy ważne'].sum()
    results['percentages'] = results['votes'] / valid_votes
    results = results.sort_values(by=['votes'], ascending=False)
    winners = results.index[:3]

    voivodeship_data = data.groupby(['Województwo']).sum()
    voivodeship_data = voivodeship_data['Głosy oddane'] / voivodeship_data['Uprawnieni']
    voivodeship_data = voivodeship_data.to_frame('turnout')
    voivodeship_data['code'] = voivodeship_data.apply(lambda row: voivodeships_codes[row.name.title()], axis=1)
    voivodeship_data['link'] = voivodeship_data.apply(lambda row: row.name.lower(), axis=1)

    template = environment.get_template(filename)
    output = template.render(
        turnout=turnout,
        results=results,
        voivodeship_data=voivodeship_data,
        winners=winners,
        candidates_images=candidates_images
    )
    os.makedirs('output', exist_ok=True)
    with open('output/index.html', 'w') as file:
        file.write(output)


def generate_voivodeship_template(voivodeship, data):
    filename = 'voivodeship.html'

    allowed = data['Uprawnieni'].sum()
    all_votes = data['Głosy oddane'].sum()
    turnout = all_votes / allowed

    constituency_data = data.groupby(['Nr okręgu']).sum()
    constituency_data = constituency_data['Głosy oddane'] / constituency_data['Uprawnieni']
    constituency_data = constituency_data.to_frame('turnout')
    constituency_data['link'] = constituency_data.index
    constituency_data.index = pd.Series(['Constituency #' + str(index) for index in constituency_data.index])
    # constituency_data['link'] = constituency_data.apply(lambda row: , axis=1)

    results = data[candidates].sum().to_frame('votes')
    valid_votes = data['Głosy ważne'].sum()
    results['percentages'] = results['votes'] / valid_votes
    results = results.sort_values(by=['votes'], ascending=False)
    winners = results.index[:3]

    template = environment.get_template(filename)
    output = template.render(
        voivodeship=voivodeship,
        constituency_data=constituency_data,
        turnout=turnout,
        results=results,
        winners=winners,
        candidates_images=candidates_images
    )

    os.makedirs('output/' + voivodeship.lower(), exist_ok=True)
    with open('output/' + voivodeship.lower() + '/index.html', 'w') as file:
        file.write(output)


def generate_constituency_template(voivodeship, constituency, data):
    filename = 'constituency.html'

    allowed = data['Uprawnieni'].sum()
    all_votes = data['Głosy oddane'].sum()
    turnout = all_votes / allowed

    powiat_data = data.groupby(['Powiat']).sum()
    powiat_data = powiat_data['Głosy oddane'] / powiat_data['Uprawnieni']
    powiat_data = powiat_data.to_frame('turnout')
    powiat_data['link'] = [link.replace(' ', '_').lower() for link in powiat_data.index]
    powiat_data.index = pd.Series(['Powiat ' + index for index in powiat_data.index])

    results = data[candidates].sum().to_frame('votes')
    valid_votes = data['Głosy ważne'].sum()
    results['percentages'] = results['votes'] / valid_votes
    results = results.sort_values(by=['votes'], ascending=False)
    winners = results.index[:3]

    template = environment.get_template(filename)
    output = template.render(
        voivodeship=voivodeship,
        constituency=constituency,
        powiat_data=powiat_data,
        turnout=turnout,
        results=results,
        winners=winners,
        candidates_images=candidates_images
    )

    os.makedirs('output/' + voivodeship.lower() + '/' + str(constituency), exist_ok=True)
    with open('output/' + voivodeship.lower() + '/' + str(constituency) + '/index.html', 'w') as file:
        file.write(output)


def generate_powiat_template(voivodeship, constituency, powiat, data):
    filename = 'powiat.html'

    allowed = data['Uprawnieni'].sum()
    all_votes = data['Głosy oddane'].sum()
    turnout = all_votes / allowed

    gmina_data = data.groupby(['Gmina']).sum()
    gmina_data = gmina_data['Głosy oddane'] / gmina_data['Uprawnieni']
    gmina_data = gmina_data.to_frame('turnout')
    gmina_data['link'] = [link.replace(' ', '_').lower() for link in gmina_data.index]

    results = data[candidates].sum().to_frame('votes')
    valid_votes = data['Głosy ważne'].sum()
    results['percentages'] = results['votes'] / valid_votes
    results = results.sort_values(by=['votes'], ascending=False)
    winners = results.index[:3]

    template = environment.get_template(filename)
    output = template.render(
        voivodeship=voivodeship,
        constituency=constituency,
        powiat=powiat,
        gmina_data=gmina_data,
        turnout=turnout,
        results=results,
        winners=winners,
        candidates_images=candidates_images
    )

    os.makedirs('output/' + voivodeship.lower() + '/' + str(constituency) + '/' + powiat.lower(), exist_ok=True)
    with open('output/' + voivodeship.lower() + '/' + str(constituency) + '/' + powiat.lower() + '/index.html', 'w') as file:
        file.write(output)


def generate_gmina_template(voivodeship, constituency, powiat, gmina, data):
    filename = 'gmina.html'

    allowed = data['Uprawnieni'].sum()
    all_votes = data['Głosy oddane'].sum()
    turnout = all_votes / allowed

    results = data[candidates].sum().to_frame('votes')
    valid_votes = data['Głosy ważne'].sum()
    results['percentages'] = results['votes'] / valid_votes
    results = results.sort_values(by=['votes'], ascending=False)
    winners = results.index[:3]

    template = environment.get_template(filename)
    output = template.render(
        voivodeship=voivodeship,
        constituency=constituency,
        powiat=powiat,
        gmina=gmina,
        turnout=turnout,
        results=results,
        winners=winners,
        candidates_images=candidates_images
    )

    os.makedirs('output/' + voivodeship.lower() + '/' + str(constituency) + '/' + powiat.lower() + '/' + gmina.replace(' ', '_').lower(), exist_ok=True)
    with open(
        'output/' + voivodeship.lower() + '/' + str(constituency) + '/' + powiat.lower() + '/' + gmina.replace(' ', '_').lower() + '/index.html',
        'w'
    ) as file:
        file.write(output)


if __name__ == '__main__':
    generate_country_template(full_data)

    voivodeships = list(full_data['Województwo'].drop_duplicates())
    for voivodeship in voivodeships:
        voivodeship_data = full_data.loc[full_data['Województwo'] == voivodeship]
        generate_voivodeship_template(voivodeship, voivodeship_data)

        constituencies = list(voivodeship_data['Nr okręgu'].drop_duplicates())
        for constituency in constituencies:
            constituency_data = voivodeship_data.loc[voivodeship_data['Nr okręgu'] == constituency]
            generate_constituency_template(voivodeship, constituency, constituency_data)

            powiats = list(constituency_data['Powiat'].drop_duplicates())
            for powiat in powiats:
                powiat_data = constituency_data.loc[constituency_data['Powiat'] == powiat]
                generate_powiat_template(voivodeship, constituency, powiat, powiat_data)

                gminas = list(powiat_data['Gmina'].drop_duplicates())
                for gmina in gminas:
                    gmina_data = constituency_data.loc[constituency_data['Gmina'] == gmina]
                    generate_gmina_template(voivodeship, constituency, powiat, gmina, gmina_data)
