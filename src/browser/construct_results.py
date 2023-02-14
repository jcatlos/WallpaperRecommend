
import pandas as pd
from querying import find_best_n

header = """<html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
    </head>

    <body>
    """

footer = """        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
</html>"""

def generate_modal(image: str, pallette: str, name: str, index: int):

    stripped_name = name.replace('.jpeg', '')

    return '''
<div class="modal fade" id="modal'''+str(index)+'''" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered" role="document">
    <div class="modal-content">
      <div class="modal-body">
        <h5>Source image:</h5>
        <img style="max-width:100%;" src="'''+image+'''">
        <h5>Color pallette:</h5>
        <img style="max-width:100%; height="50px;" src="'''+pallette+'''">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <a href="'''+name+'''" role="button" class="btn btn-primary">Find similar</a>
        <a href="https://www.pexels.com/photo/'''+stripped_name+'''" role="button" class="btn btn-success">Get original image</a>
      </div>
    </div>
  </div>
</div>
    '''

def generate_modals(results):

    agg = ""
    for i in range(1,10):

        index = i
        if index == 5: index = 0
        elif index > 5: index -= 1

        agg += generate_modal(
            str(results.iloc[index]['image_path']), 
            str(results.iloc[index]['pallette_path']),
            str(results.iloc[index]['image_path']).split('\\')[-1],
            index
        )
        
    return agg
    

def construct_results(
    center_image_path: str,
    center_image_pallette: str,
    image1_path: str,
    image1_pallette: str,
    image2_path: str,
    image2_pallette: str,
    image3_path: str,
    image3_pallette: str,
    image4_path: str,
    image4_pallette: str,
    image5_path: str,
    image5_pallette: str,
    image6_path: str,
    image6_pallette: str,
    image7_path: str,
    image7_pallette: str,
    image8_path: str,
    image8_pallette: str,
):
    return  '''<div id="suggestions" class="container">
    <h1>Results</h1>
    <a href="/" class="btn btn-primary">Back to main menu</a>
    <div class="row">
        <!-- pridat divom px-0 class aby neboli medzery -->
        <div class="col-4 px-0" data-toggle="modal" data-target="#modal1">
            <img style="width:300px; height:300px;" class="img-fluid" src="''' + image1_path + '''">
            <img style="width:300px; height:40px;" class="img-fluid" src="''' + image1_pallette + '''">
        </div>
        <div class="col-4 px-0" data-toggle="modal" data-target="#modal2">
            <img style="width:300px; height:300px;" class="img-fluid" src="''' + image2_path + '''">
            <img style="width:300px; height:40px;" class="img-fluid" src="''' + image2_pallette + '''">
        </div>
        <div class="col-4 px-0" data-toggle="modal" data-target="#modal3">
            <img style="width:300px; height:300px;" class="img-fluid" src="''' + image3_path + '''">
            <img style="width:300px; height:40px;" class="img-fluid" src="''' + image3_pallette + '''">
        </div>
    </div>
    <div class="row"> 
        <div class="col-4 px-0" data-toggle="modal" data-target="#modal4">
            <img style="width:300px; height:300px;" class="img-fluid" src="''' + image4_path + '''">
            <img style="width:300px; height:40px;" class="img-fluid" src="''' + image4_pallette + '''">
        </div>
        <div id="best" class="col-4 px-0" data-toggle="modal" data-target="#modal0">
            <img style="width:300px; height:300px;" class="img-fluid" src="''' + center_image_path + '''">
            <img style="width:300px; height:40px;" class="img-fluid" src="''' + center_image_pallette + '''">
        </div>
        <div class="col-4 px-0" data-toggle="modal" data-target="#modal5">
            <img style="width:300px; height:300px;" class="img-fluid" src="''' + image5_path + '''">
            <img style="width:300px; height:40px;" class="img-fluid" src="''' + image5_pallette + '''">
        </div>
    </div>
    <div class="row">
        <div class="col-4 px-0" data-toggle="modal" data-target="#modal6">
            <img style="width:300px; height:300px;" class="img-fluid" src="''' + image6_path + '''">
            <img style="width:300px; height:40px;" class="img-fluid" src="''' + image6_pallette + '''">
        </div>
        <div class="col-4 px-0"  data-toggle="modal" data-target="#modal7">
            <img style="width:300px; height:300px;" class="img-fluid" src="''' + image7_path + '''">
            <img style="width:300px; height:40px;" class="img-fluid" src="''' + image7_pallette + '''">
        </div>
        <div class="col-4 px-0" data-toggle="modal" data-target="#modal8">
            <img style="width:300px; height:300px;" class="img-fluid" src="''' + image8_path + '''">
            <img style="width:300px; height:40px;" class="img-fluid" src="''' + image8_pallette + '''">
        </div>
    </div>
</div>'''

def construct_result_page(results: pd.DataFrame):

    results_html = construct_results(
        str(results.iloc[0]['image_path']),
        str(results.iloc[0]['pallette_path']),
        str(results.iloc[1]['image_path']),
        str(results.iloc[1]['pallette_path']),
        str(results.iloc[2]['image_path']),
        str(results.iloc[2]['pallette_path']),
        str(results.iloc[3]['image_path']),
        str(results.iloc[3]['pallette_path']),
        str(results.iloc[4]['image_path']),
        str(results.iloc[4]['pallette_path']),
        str(results.iloc[5]['image_path']),
        str(results.iloc[5]['pallette_path']),
        str(results.iloc[6]['image_path']),
        str(results.iloc[6]['pallette_path']),
        str(results.iloc[7]['image_path']),
        str(results.iloc[7]['pallette_path']),
        str(results.iloc[8]['image_path']),
        str(results.iloc[8]['pallette_path']),
    )

    return header + results_html + generate_modals(results) + footer
