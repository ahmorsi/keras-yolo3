from googleapiclient import discovery
from googleapiclient import errors
# Time is for waiting until the request finishes.
import time

projectID = 'projects/{}'.format('yolo3')
modelName = 'tf_yolo3_model'
modelID = '{}/models/{}'.format(projectID, modelName)
versionName = 'test_version'
versionDescription = 'Only for testing'
trainedModelLocation = ''#Todo add gs bucket path for SavedModel
#runtimeVersion = '1.12'
#pythonVersion = '3.5'

# Optional, to use quad core CPUs for online prediction
#machineType = 'mls1-c4-m2'

ml = discovery.build('ml', 'v1')

# Create a dictionary with the fields from the request body.
# Including the 'machineType' field is optional
requestDict = {'name': versionName,
  'description': versionDescription,
  'deploymentUri': trainedModelLocation}

# Create a request to call projects.models.create.
request = ml.projects().models().create(parent=projectID,
                            body=requestDict)

# Make the call.
try:
    response = request.execute()
    # Get the operation name.
    operationID = response['name']
    # Any additional code on success goes here (logging, etc.)

except errors.HttpError as err:
    # Something went wrong, print out some information.
    print('There was an error creating the model.' +
        ' Check the details:')
    print(err._get_reason())

    # Clear the response for next time.
    response = None


done = False
request = ml.projects().operations().get(name=operationID)

while not done:
    response = None

    # Wait for 300 milliseconds.
    time.sleep(0.3)

    # Make the next call.
    try:
        response = request.execute()

        # Check for finish.
        done = response.get('done', False)

    except errors.HttpError as err:
        # Something went wrong, print out some information.
        print('There was an error getting the operation.' +
              'Check the details:')
        print(err._get_reason())
        done = True