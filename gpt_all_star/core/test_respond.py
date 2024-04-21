from gpt_all_star.core.respond import Respond

def test_deploy(mocker):
    respond = Respond(...)
    mocker.patch.object(respond.copilot, 'run_command')
    
    result = list(respond.deploy())
    
    assert len(result) == 2
    assert "Successfully deployed" in result[1]["messages"][0].message

def test_execute(mocker):
    respond = Respond(...)
    mocker.patch.object(respond.copilot, 'run_command', return_value="http://test.url")
    
    result = list(respond.execute())
    
    assert len(result) == 2 
    assert "Execute command" in result[0]["messages"][0].message
    assert "http://test.url" in result[1]["messages"][0].message