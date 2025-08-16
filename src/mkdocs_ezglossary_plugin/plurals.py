plurals = {
    'en': {
        # Regular plurals
        's$': [''],           # cats -> cat
        'es$': ['', 'is'],    # boxes -> box, analysis -> analyses
        'ies$': ['y'],        # cities -> city
        'ves$': ['f', 'fe'],  # wolves -> wolf, knives -> knife
        'ses$': ['s'],        # buses -> bus
        'zes$': ['z'],        # quizzes -> quiz
        
        # Latin/Greek plurals
        'i$': ['us'],         # fungi -> fungus
        'ae$': ['a'],         # larvae -> larva
        'a$': ['on', 'um'],   # phenomena -> phenomenon, data -> datum
        
        # Irregular plurals
        'children$': ['child'],
        'geese$': ['goose'],
        'men$': ['man'],      # also handles: women -> woman
        'teeth$': ['tooth'],
        'feet$': ['foot'],
        'mice$': ['mouse'],
        'people$': ['person'],
        'oxen$': ['ox'],
        'indices$': ['index'],
        'matrices$': ['matrix'],
        'vertices$': ['vertex'],
        'appendices$': ['appendix'],
    },
    
    'es': {
        # Regular plurals
        'es$': [''],          # árboles -> árbol, coches -> coche
        's$': [''],           # casas -> casa
        
        # Special cases with accent marks
        'enes$': ['en'],      # exámenes -> examen
        'ones$': ['ón'],      # situaciones -> situación
        'eses$': ['és'],      # ingleses -> inglés
        
        # Irregular plurals
        'ces$': ['z'],        # peces -> pez
        
        # Special plurals ending in -es
        'ís$': ['í'],         # rubís -> rubí
        'ús$': ['ú'],         # bambús -> bambú
    },
    
    'de': {
        # Regular plurals
        'en$': [''],          # Katzen -> Katze
        'n$': [''],           # Frauen -> Frau
        'e$': [''],           # Hunde -> Hund
        'er$': [''],          # Kinder -> Kind
        
        # Umlaut plurals (need to be handled in code)
        'äuser$': ['aus'],    # Häuser -> Haus
        'äume$': ['aum'],     # Bäume -> Baum
        'änder$': ['and'],    # Länder -> Land
        'äfte$': ['aft'],     # Kräfte -> Kraft
        'ücher$': ['uch'],    # Bücher -> Buch
        'öfe$': ['of'],       # Höfe -> Hof
        
        # Special cases
        'ien$': ['ium'],      # Laboratorien -> Laboratorium
        'a$': ['um'],         # Musea -> Museum
        'i$': ['us'],         # Alumni -> Alumnus
    },
    
    'fr': {
        # Regular plurals
        's$': [''],           # maisons -> maison
        'x$': [''],           # chevaux -> cheval
        'aux$': ['al'],       # journaux -> journal
        'eaux$': ['eau'],     # tableaux -> tableau
        
        # Special endings
        'eux$': ['eu'],       # jeux -> jeu
        'oux$': ['ou'],       # bijoux -> bijou
        
        # Irregular plurals that end in -s
        'ils$': ['il'],       # fils -> fil
        'ails$': ['ail'],     # travails -> travail
        
        # Academic terms (from Latin)
        'a$': ['um'],         # média -> médium
        'i$': ['us'],         # alumni -> alumnus
        'ae$': ['a'],         # algae -> alga
    }
}
