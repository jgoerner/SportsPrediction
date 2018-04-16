from features import (
    create_team_triples,
)

def derive_features():
    # explicitly define features to be derived
    features = [
        create_team_triples
    ]
    
    print("\n" + "/"*112)
    print("/" + " "*47 + "Deriving Features" + " "*46 + "/")
    print("/"*112 + "\n\n")
    
    for f in features:
        print("#"*(len(f.__name__)+13))
        print("# Deriving {} #".format(f.__name__))
        print("#"*(len(f.__name__)+13))
        try:
            t_name = f()
            print("Created\n\n")
        except ValueError as e:
            print(e, end="\n\n")

if __name__ == "__main__":
    derive_features()
