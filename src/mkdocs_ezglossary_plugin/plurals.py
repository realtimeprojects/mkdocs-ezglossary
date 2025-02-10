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
    }
}
