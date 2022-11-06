import brain
from flask import Flask, jsonify ,request , json

#constants
app=Flask(__name__)

@app.route('/get_family_tree',methods=['POST'])
def get_family_tree():
    name_of_the_voter=request.json['name_of_the_voter']
    kin_name_voter=request.json['kin_name_voter']
    dob_provided=request.json['dob_provided']
    dob_voter=request.json['dob_voter']
    age=request.json['age']
    gender_provided=request.json['gender_provided']
    state=request.json['state']
    district=request.json['district']
    assembly_const=request.json['assembly_const']
    manually_input_captcha=request.json['manually_input_captcha']
    print(name_of_the_voter, kin_name_voter, dob_provided, dob_voter, age, gender_provided, state
                           , district, assembly_const, manually_input_captcha)

    brain.extract_larger_dataset(name_of_the_voter, kin_name_voter, dob_provided, dob_voter, age, gender_provided, state
                          , district, assembly_const, manually_input_captcha)
    dic_of_names_here=brain.extract_data_from_larger_dataset()
    # print(dic_of_names_here)
    f_t=brain.return_family_tree(name_of_the_voter,dic_of_names_here)
    f_t = json.dumps(f_t, indent=2)

    return f_t

if __name__=="__main__":
    app.run(debug=True)
