from features import (
    create_player_college_triples,
    create_team_triples,
)

def derive_features():
    # explicitly define features to be derived
    features = [
        create_player_college_triples,
        create_team_triples,
    ]
    
    print("\n" + "/"*112)
    print("/" + " "*46 + "Processing Features" + " "*45 + "/")
    print("/"*112 + "\n\n")
    
    for f in features:
        print("#"*(len(f.__name__)+15))
        print("# Processing {} #".format(f.__name__))
        print("#"*(len(f.__name__)+15))
        try:
            t_name = f()
            print("Created\n\n")
        except ValueError as e:
            print(e, end="\n\n")

if __name__ == "__main__":
    derive_features()
