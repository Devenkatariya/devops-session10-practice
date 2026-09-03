"""Main application module."""

def calculate_deployment_risk(changes: dict) -> str:
    """
    Calculate risk level of a deployment based on changes.

    Args:
        changes: dict with keys 'files_changed',
                 'lines_changed', 'has_tests', 'has_review'

    Returns:
        Risk level: 'low', 'medium', or 'high'
    """
    score = 0

    if changes.get('files_changed', 0) > 20:
        score += 2
    elif changes.get('files_changed', 0) > 5:
        score += 1

    if changes.get('lines_changed', 0) > 500:
        score += 2
    elif changes.get('lines_changed', 0) > 100:
        score += 1

    if not changes.get('has_tests', False):
        score += 2

    if not changes.get('has_review', False):
        score += 3

    if score >= 5:
        return 'high'
    elif score >= 3:
        return 'medium'
    else:
        return 'low'

if __name__ == '__main__':
    example = {
        'files_changed': 3,
        'lines_changed': 50,
        'has_tests': True,
        'has_review': True
    }
    risk = calculate_deployment_risk(example)
    print(f"Deployment risk: {risk}")
