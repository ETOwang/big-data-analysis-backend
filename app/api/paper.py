from flask import Blueprint, request, jsonify
from app.models import Paper, Citation

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
            Paper.title.contains(query)
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

        # Fetch citations and similar papers (assuming relationships are defined in the Paper model)
        citations = []
        base_query = Paper.query.filter(
            Paper.abstract.contains(paper.title)
        )
        similar_papers = base_query.paginate()
        base_query = Citation.query.filter(
            Citation.first == paper.id
        )
        for (first, second) in base_query.paginate():
            citations.append(Paper.query.get_or_404(second))

        # Format citations
        formatted_citations = [{
            'title': citation.title,
            'year': citation.year.year if citation.year else None
        } for citation in citations]

        # Format similar papers
        formatted_similar_papers = [{
            'title': similar.title,
            'abstractPreview': similar.abstract[:200] + '...' if similar.abstract else '',
            'year': similar.year.year if similar.year else None
        } for similar in similar_papers]

        # Basic paper info
        paper_data = {
            'title': paper.title,
            'abstract': paper.abstract,
            'year': paper.year.year if paper.year else None,
            'citations': formatted_citations,
            'similarPapers': formatted_similar_papers,
            'category': paper.category if paper.category else "",
        }
        print(formatted_similar_papers)
        print(formatted_citations)
        return jsonify({
            'status': 'success',
            'data': paper_data
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
