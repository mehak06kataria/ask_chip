
CHIP_TEST_PRIVATE_CHANNEL_ID = 'C03HA2B21RP'

SAMPLE_SLACK_SEARCH_OUTPUT = [{
      'content' : 'Our team ETA support sessioned dashboard suddenly became inaccessible (happened ~ a week ago). Is any other team facing the same issue?',
      'link' : 'https://rippling.slack.com/archives/C1Y2YN21L/p1648723566544669',
},
{
      'content' : 'hi team getting the error game game',
      'link' : 'https://rippling.slack.com/archives/C02AJAS27V5/p1639745445281300',
},
{
      'content' : 'Please fill in the details for your Team Names, Projects, Descriptions and Mentors in the file by today EOD before todays session',
      'link' : 'https://rippling.slack.com/archives/C02S17K8NUX/p1653020239627189',
}]

SAMPLE_DRIVE_SEARCH_OUTPUT = [{
      'content' : 'To modify and refactor suta_state_estimator.py for better estimation accuracy, game session code, code readability and to improve debugging.',
      'link' : 'https://docs.google.com/document/d/1Q9xC02S17K8NUX9hIKZx7J2QtmOadR8j24gKWudrDQ/edit',
},
{
      'content' : 'If there’s a situation when the self employed gamer are not covered for WA PFML, there’s no direct payroll setting to avoid calculating tax for the employee.',
      'link' : 'https://docs.google.com/document/d/1Q9xvVYxTTlCr6C02S17K8NUX7J2QtmR8j24gKWudrDQ/edit',
},
{
      'content' : 'Risk for plating games. This may occur if the work state for the employee is not WA. Ask the IM to change the work location to “WA”, assign the “Risk Code” and then change it back to “Remote”.',
      'link' : 'https://docs.google.com/document/d/1Q9C02S17K8NUXffs2L9hIKZx7J2QtmOR8j24gKWudrDQ/edit',
}]

SAMPLE_CONFLUENCE_SEARCH_OUTPUT = [{
      'content' : 'Please follow the instructions on the backend and the frontend gaming repositories to setup.',
      'link' : 'https://rippling.atlassian.net/wiki/spaces/ENG/pages/664928265/Engineer+s+Starter+Kit',
},
{
      'content' : 'As a developer, you have to make changes in the local, test that, replicate the game bug, monitor the production sessions, etc.',
      'link' : 'https://rippling.atlassian.net/wiki/spaces/ENG/pages/678395920/Staging+staff+user+access',
},
{
      'content' : 'Following Tech Session Talks are recommended for new hires to watch. Watch them at 2x, so you can later refer to it when you will need them in your work.',
      'link' : 'https://rippling.atlassian.net/wiki/spaces/ENG/pages/2834857987/Important+Tech+Talks+for+new+hires',
}]


SAMPLE_HARDCODED_RESULT = [{
                        'content': 'To modify and refactor suta_state_estimator.py for better estimation accuracy, game session code, code readability and to improve debugging.',
                        'link': 'https://docs.google.com/document/d/1Q9xC02S17K8NUX9hIKZx7J2QtmOadR8j24gKWudrDQ/edit',
                        'type': 'drive'},
                    {
                        'content': 'Our team ETA support sessioned dashboard suddenly became inaccessible (happened ~ a week ago). Is any other team facing the same issue?',
                        'link': 'https://rippling.slack.com/archives/C1Y2YN21L/p1648723566544669', 'type': 'slack'},
                    {'content': 'hi team getting the error game game',
                     'link': 'https://rippling.slack.com/archives/C02AJAS27V5/p1639745445281300', 'type': 'slack'},
                    {
                        'content': 'Please fill in the details for your Team Names, Projects, Descriptions and Mentors in the file by today EOD before todays session',
                        'link': 'https://rippling.slack.com/archives/C02S17K8NUX/p1653020239627189', 'type': 'slack'},
                    {
                        'content': 'If there’s a situation when the self employed gamer are not covered for WA PFML, there’s no direct payroll setting to avoid calculating tax for the employee.',
                        'link': 'https://docs.google.com/document/d/1Q9xvVYxTTlCr6C02S17K8NUX7J2QtmR8j24gKWudrDQ/edit',
                        'type': 'drive'},
                    {
                        'content': 'Risk for plating games. This may occur if the work state for the employee is not WA. Ask the IM to change the work location to “WA”, assign the “Risk Code” and then change it back to “Remote”.',
                        'link': 'https://docs.google.com/document/d/1Q9C02S17K8NUXffs2L9hIKZx7J2QtmOR8j24gKWudrDQ/edit',
                        'type': 'drive'},
                    {
                        'content': 'Please follow the instructions on the backend and the frontend gaming repositories to setup.',
                        'link': 'https://rippling.atlassian.net/wiki/spaces/ENG/pages/664928265/Engineer+s+Starter+Kit',
                        'type': 'confluence'},
                    {
                        'content': 'As a developer, you have to make changes in the local, test that, replicate the game bug, monitor the production sessions, etc.',
                        'link': 'https://rippling.atlassian.net/wiki/spaces/ENG/pages/678395920/Staging+staff+user+access',
                        'type': 'confluence'},
                    {
                        'content': 'Following Tech Session Talks are recommended for new hires to watch. Watch them at 2x, so you can later refer to it when you will need them in your work.',
                        'link': 'https://rippling.atlassian.net/wiki/spaces/ENG/pages/2834857987/Important+Tech+Talks+for+new+hires',
                        'type': 'confluence'}]
