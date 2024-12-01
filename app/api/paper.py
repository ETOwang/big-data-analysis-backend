from flask import Blueprint, request, jsonify
from app.models import Paper

search_papers = Blueprint('search_papers', __name__)


@search_papers.route('/api/search', methods=['GET'])
def search():
    try:
        # Get query parameters
        query = request.args.get('query', '')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 10))
        sort = request.args.get('sort', 'year')  # Default sort by year

        # Build base query
        base_query = Paper.query.filter(
            Paper.title.contains(query) | Paper.abstract.contains(query)
        )

        # Apply sorting
        if sort == 'year':
            base_query = base_query.order_by(Paper.year.desc())
        elif sort == 'relevance':
            # Implement relevance sorting logic if needed
            pass

        # Execute paginated query
        papers = base_query.paginate(page=page, per_page=size, error_out=False)

        # Format results
        results = [{
            'paperId': paper.id,
            'title': paper.title,
            'abstract': paper.abstract[:200] + '...' if paper.abstract else '',
            'year': paper.year.year if paper.year else None,
        } for paper in papers.items]

        return jsonify({
            'status': 'success',
            'data': results,
            'totalResults': papers.total,
            'page': page,
            'pageSize': size
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@search_papers.route('/api/papers/<string:id>', methods=['GET'])
def get_paper(id):
    try:
        paper = Paper.query.get_or_404(id)

        # Basic paper info
        paper_data = {
            'paperId': paper.id,
            'title': paper.title,
            'abstract': paper.abstract,
            'year': paper.year.year if paper.year else None,
            'category': paper.category
        }

        return jsonify({
            'status': 'success',
            'data': paper_data
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
