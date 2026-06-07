import pandas as pd
import streamlit as st


@st.cache_data
def load_garments():
    data = [
        {
            "garment_id": 1,
            "name": "Dior New Look Suit",
            "designer": "Christian Dior",
            "era": "1950s",
            "material": "Wool Crepe",
            "condition": "Excellent",
            "description": "A stunning example of Dior's revolutionary 1947 New Look silhouette. Nipped waist, padded hips, and a sweeping midi skirt that redefined post-war femininity. Original Dior label intact.",
            "size": "FR 38",
            "style_tags": ["New Look", "Couture", "Structured", "Feminine"],
            "icon": "👗",
            "listing_status": "Available",
            "celebrity": "Audrey Hepburn (rumored)",
            "provenance": [
                {"year": 1952, "event": "Runway Debut", "type": "Runway", "desc": "Showcased at the autumn Dior Haute Couture presentation in Paris."},
                {"year": 1958, "event": "Museum Exhibition", "type": "Exhibition", "desc": "Part of 'The Art of Fashion' exhibition at the V&A, London."},
                {"year": 1965, "event": "Private Sale", "type": "Sale", "desc": "Acquired by a private Italian collector from a Paris auction house."},
            ]
        },
        {
            "garment_id": 2,
            "name": "Balenciaga Cocoon Coat",
            "designer": "Cristóbal Balenciaga",
            "era": "1950s",
            "material": "Silk Gazar",
            "condition": "Good",
            "description": "Balenciaga's iconic cocoon silhouette — a masterclass in architectural dressmaking. The coat stands away from the body, creating a perfect ovoid form that challenged all conventions.",
            "size": "FR 40",
            "style_tags": ["Architectural", "Avant-garde", "Couture"],
            "icon": "🧥",
            "listing_status": "Sold",
            "celebrity": "Grace Kelly",
            "provenance": [
                {"year": 1955, "event": "Eisa Madrid Salon Debut", "type": "Runway", "desc": "Presented at Balenciaga's Madrid salon during the spring collection."},
                {"year": 1961, "event": "Grace Kelly Photographed", "type": "Celebrity", "desc": "Grace Kelly photographed wearing the piece at a Monaco charity gala."},
            ]
        },
        {
            "garment_id": 3,
            "name": "Halston Ultrasuede Shirt Dress",
            "designer": "Halston",
            "era": "1970s",
            "material": "Ultrasuede",
            "condition": "Good",
            "description": "The garment that defined 1970s American minimalism. Halston's Ultrasuede shirt dress democratized luxury — washable, comfortable, and impeccably chic. Studio 54 staple.",
            "size": "US 8",
            "style_tags": ["Minimalist", "American", "Studio 54", "Day-to-Night"],
            "icon": "👘",
            "listing_status": "Available",
            "celebrity": "Bianca Jagger",
            "provenance": [
                {"year": 1972, "event": "First Collection Drop", "type": "Runway", "desc": "Debuted as part of Halston's groundbreaking 1972 ready-to-wear line."},
                {"year": 1977, "event": "Studio 54 Appearance", "type": "Celebrity", "desc": "Worn by Bianca Jagger at Studio 54's legendary New Year's Eve party."},
            ]
        },
        {
            "garment_id": 4,
            "name": "Vivienne Westwood Punk Corset",
            "designer": "Vivienne Westwood",
            "era": "1980s",
            "material": "Brocade & Steel Boning",
            "condition": "Fair",
            "description": "From Westwood's legendary 'Time Machine' collection. This corset encapsulates the punk-meets-historical-fashion collision that made Westwood a revolutionary force. Safety-pin details original.",
            "size": "UK 10",
            "style_tags": ["Punk", "Subversive", "Historical Revival", "Corsetry"],
            "icon": "🪡",
            "listing_status": "Available",
            "celebrity": "Siouxsie Sioux",
            "provenance": [
                {"year": 1984, "event": "Time Machine Collection", "type": "Runway", "desc": "Central piece of Westwood's Time Machine runway presentation."},
                {"year": 1986, "event": "Victoria & Albert Acquisition Attempt", "type": "Exhibition", "desc": "Considered for permanent acquisition by the V&A curatorial board."},
            ]
        },
        {
            "garment_id": 5,
            "name": "Chanel 2.55 Little Black Dress",
            "designer": "Coco Chanel",
            "era": "1960s",
            "material": "Jersey Knit",
            "condition": "Excellent",
            "description": "The definitive LBD from Chanel's 1960s ready-to-wear line. Slightly flared A-line silhouette, three-quarter sleeves, and the signature Chanel gilt chain at the waist. Timeless.",
            "size": "FR 36",
            "style_tags": ["Classic", "LBD", "French Chic", "Timeless"],
            "icon": "🖤",
            "listing_status": "Available",
            "celebrity": "Jackie Kennedy (similar)",
            "provenance": [
                {"year": 1963, "event": "Chanel Boutique Release", "type": "Sale", "desc": "Released through the original Rue Cambon boutique, Paris."},
                {"year": 1971, "event": "Estate Sale", "type": "Sale", "desc": "Acquired at Paris estate sale following original owner's passing."},
                {"year": 2005, "event": "Fashion Institute Loan", "type": "Exhibition", "desc": "On loan to FIT New York for 'Little Black Dress' retrospective."},
            ]
        },
        {
            "garment_id": 6,
            "name": "Issey Miyake Pleats Please Set",
            "designer": "Issey Miyake",
            "era": "1990s",
            "material": "Polyester Pleat",
            "condition": "Excellent",
            "description": "Miyake's Pleats Please line revolutionized fashion technology — permanently pleated polyester that never wrinkles, travels perfectly, and maintains its sculptural form. A wearable artwork.",
            "size": "JP 2",
            "style_tags": ["Japanese", "Technical", "Sculptural", "Wearable Art"],
            "icon": "🌀",
            "listing_status": "Available",
            "celebrity": "None",
            "provenance": [
                {"year": 1993, "event": "Tokyo Launch", "type": "Runway", "desc": "Premiered at the Tokyo International Fashion Week autumn collection."},
                {"year": 1998, "event": "MoMA Inclusion", "type": "Exhibition", "desc": "Included in MoMA's 'Workspheres' design exhibition as functional art."},
            ]
        },
        {
            "garment_id": 7,
            "name": "Yves Saint Laurent Le Smoking Tuxedo",
            "designer": "Yves Saint Laurent",
            "era": "1970s",
            "material": "Wool Gabardine",
            "condition": "Good",
            "description": "YSL's iconic 'Le Smoking' — the first tuxedo designed for women, debuted in 1966. This 1970s iteration features a slightly wider lapel reflecting the era's aesthetic evolution. Revolutionary.",
            "size": "FR 38",
            "style_tags": ["Power Dressing", "Androgynous", "French", "Iconic"],
            "icon": "🎩",
            "listing_status": "Available",
            "celebrity": "Nan Kempner",
            "provenance": [
                {"year": 1975, "event": "YSL Rive Gauche Launch", "type": "Runway", "desc": "Part of the Rive Gauche ready-to-wear autumn/winter collection."},
                {"year": 1979, "event": "Vogue Paris Feature", "type": "Media", "desc": "Featured in Vogue Paris editorial photographed by Helmut Newton."},
            ]
        },
        {
            "garment_id": 8,
            "name": "Comme des Garçons Deconstructed Jacket",
            "designer": "Comme des Garçons",
            "era": "1990s",
            "material": "Wool & Linen",
            "condition": "Fair",
            "description": "Rei Kawakubo's radical deconstruction at its finest — raw edges, exposed seams, asymmetric lapels. This piece embodies the 1990s anti-fashion movement that changed the industry forever.",
            "size": "JP 3",
            "style_tags": ["Deconstructed", "Avant-garde", "Japanese", "Anti-Fashion"],
            "icon": "🧣",
            "listing_status": "Available",
            "celebrity": "None",
            "provenance": [
                {"year": 1995, "event": "Paris Runway", "type": "Runway", "desc": "Shown at the controversial CdG Paris show that divided critics."},
                {"year": 2001, "event": "Kyoto Costume Institute Acquisition", "type": "Museum", "desc": "Sister piece acquired by the Kyoto Costume Institute for permanent collection."},
            ]
        },
    ]
    return pd.DataFrame(data)


@st.cache_data
def load_listings():
    data = [
        {"listing_id": 1, "garment_id": 1, "garment_name": "Dior New Look Suit", "designer": "Christian Dior", "era": "1950s", "price": 12500, "seller": "Maison Vintage Paris", "condition": "Excellent", "icon": "👗", "verified": True},
        {"listing_id": 2, "garment_id": 3, "garment_name": "Halston Ultrasuede Shirt Dress", "designer": "Halston", "era": "1970s", "price": 3200, "seller": "Studio 54 Relics", "condition": "Good", "icon": "👘", "verified": True},
        {"listing_id": 3, "garment_id": 4, "garment_name": "Vivienne Westwood Punk Corset", "designer": "Vivienne Westwood", "era": "1980s", "price": 5800, "seller": "Punk Archive UK", "condition": "Fair", "icon": "🪡", "verified": False},
        {"listing_id": 4, "garment_id": 5, "garment_name": "Chanel Little Black Dress", "designer": "Coco Chanel", "era": "1960s", "price": 18000, "seller": "Maison Vintage Paris", "condition": "Excellent", "icon": "🖤", "verified": True},
        {"listing_id": 5, "garment_id": 6, "garment_name": "Issey Miyake Pleats Please Set", "designer": "Issey Miyake", "era": "1990s", "price": 1800, "seller": "Tokyo Vintage House", "condition": "Excellent", "icon": "🌀", "verified": True},
        {"listing_id": 6, "garment_id": 7, "garment_name": "YSL Le Smoking Tuxedo", "designer": "Yves Saint Laurent", "era": "1970s", "price": 9500, "seller": "Rive Gauche Antiques", "condition": "Good", "icon": "🎩", "verified": True},
        {"listing_id": 7, "garment_id": 8, "garment_name": "CdG Deconstructed Jacket", "designer": "Comme des Garçons", "era": "1990s", "price": 4200, "seller": "Tokyo Vintage House", "condition": "Fair", "icon": "🧣", "verified": False},
    ]
    return pd.DataFrame(data)


@st.cache_data
def load_provenance_events():
    data = [
        {"event_id": 1, "event_name": "Dior Automne Collection Runway", "date": "1952-10-14", "event_type": "Runway Show", "description": "Christian Dior's autumn collection showcased in the grand salons of Avenue Montaigne. Models walked in the signature New Look silhouette that had already transformed global fashion.", "garment": "Dior New Look Suit", "location": "Paris, France", "celebrity": None},
        {"event_id": 2, "event_name": "Grace Kelly Monaco Gala", "date": "1961-04-19", "event_type": "Celebrity", "description": "Princess Grace of Monaco wore the Balenciaga Cocoon Coat to a charity gala in Monte Carlo. Photographs appeared in Paris Match the following week, igniting global demand.", "garment": "Balenciaga Cocoon Coat", "location": "Monaco", "celebrity": "Grace Kelly"},
        {"event_id": 3, "event_name": "V&A — The Art of Fashion Exhibition", "date": "1958-06-01", "event_type": "Museum Exhibition", "description": "The Victoria and Albert Museum's landmark fashion retrospective displayed over 200 garments spanning a century of couture. The Dior suit was a centrepiece of the post-war section.", "garment": "Dior New Look Suit", "location": "London, UK", "celebrity": None},
        {"event_id": 4, "event_name": "Studio 54 New Year's Eve", "date": "1977-12-31", "event_type": "Celebrity", "description": "Bianca Jagger arrived at Studio 54's legendary NYE party wearing the Halston Ultrasuede dress. The image became one of the defining photographs of 1970s New York nightlife.", "garment": "Halston Ultrasuede Shirt Dress", "location": "New York, USA", "celebrity": "Bianca Jagger"},
        {"event_id": 5, "event_name": "Westwood Time Machine — London Fashion Week", "date": "1984-03-15", "event_type": "Runway Show", "description": "Vivienne Westwood's Time Machine collection fused punk attitude with Victorian corsetry. Fashion critics were divided; history has vindicated it as a watershed moment in British fashion.", "garment": "Vivienne Westwood Punk Corset", "location": "London, UK", "celebrity": None},
        {"event_id": 6, "event_name": "FIT New York — Little Black Dress Retrospective", "date": "2005-09-10", "event_type": "Museum Exhibition", "description": "The Fashion Institute of Technology mounted an ambitious retrospective on the LBD from Chanel's 1926 original to contemporary iterations. The 1963 Chanel piece was the anchor of the modern section.", "garment": "Chanel Little Black Dress", "location": "New York, USA", "celebrity": None},
        {"event_id": 7, "event_name": "Vogue Paris — Helmut Newton Shoot", "date": "1979-09-01", "event_type": "Media", "description": "Helmut Newton's iconic Vogue Paris editorial 'Le Smoking Redux' featured four models in YSL tuxedos against stark Parisian backdrops. The images permanently associated the tuxedo with female power.", "garment": "YSL Le Smoking Tuxedo", "location": "Paris, France", "celebrity": None},
        {"event_id": 8, "event_name": "MoMA Workspheres Exhibition", "date": "2001-02-08", "event_type": "Museum Exhibition", "description": "The Museum of Modern Art included the Miyake Pleats Please set in Workspheres, an exhibition exploring the relationship between design and work. It was displayed alongside furniture and industrial objects.", "garment": "Issey Miyake Pleats Please Set", "location": "New York, USA", "celebrity": None},
    ]
    return pd.DataFrame(data)


@st.cache_data
def load_pending_submissions():
    data = [
        {"id": 1, "garment": "Pucci Print Shift Dress", "designer": "Emilio Pucci", "era": "1960s", "seller": "marco.bianchi@vintage.it", "submitted": "2025-03-10", "status": "Pending"},
        {"id": 2, "garment": "Courrèges Space Age Dress", "designer": "André Courrèges", "era": "1960s", "seller": "retro.finds@uk.com", "submitted": "2025-03-12", "status": "Pending"},
        {"id": 3, "garment": "Ossie Clark Crepe Dress", "designer": "Ossie Clark", "era": "1970s", "seller": "london.vintage@post.com", "submitted": "2025-03-14", "status": "Pending"},
        {"id": 4, "garment": "Ungaro Ruffled Gown", "designer": "Emanuel Ungaro", "era": "1980s", "seller": "paris.archive@mail.fr", "submitted": "2025-03-15", "status": "Pending"},
    ]
    return pd.DataFrame(data)