import pytest
from git_commits_extractor.main import extract_commits

def test_extract_commits(mocker):
    mock_repo = mocker.patch('git_commits_extractor.main.git.Repo')
    mock_repo.return_value.iter_commits.return_value = [
        mocker.Mock(author=mocker.Mock(email='test@example.com'), 
                    authored_datetime=mocker.Mock(year=2023, month=10, day=1), 
                    hexsha='abc123', 
                    message='Initial commit'),
        mocker.Mock(author=mocker.Mock(email='test@example.com'), 
                    authored_datetime=mocker.Mock(year=2023, month=10, day=2), 
                    hexsha='def456', 
                    message='Second commit'),
        mocker.Mock(author=mocker.Mock(email='other@example.com'), 
                    authored_datetime=mocker.Mock(year=2023, month=10, day=3), 
                    hexsha='ghi789', 
                    message='Other commit'),
    ]
    
    commits = extract_commits(since='2023-10-01', repo_path='fake/path', format='table')
    
    assert len(commits) == 2
    assert commits[0].hexsha == 'abc123'
    assert commits[1].hexsha == 'def456'