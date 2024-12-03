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
            Paper.abstract.contains(paper.title.split(' ')[0])
        )
        similar_papers = base_query.paginate()
        base_query = Citation.query.filter(
            Citation.first == paper.id
        )
        for item in base_query.paginate().items:
            citations.append(Paper.query.get_or_404(item.second))
        # Format citations
        formatted_citations = [{
            'paperId': citation.id,
            'title': citation.title,
            'year': citation.year.year if citation.year else None
        } for citation in citations]

        # Format similar papers
        formatted_similar_papers = [{
            'paperId': similar.id,
            'title': similar.title,
            'abstractPreview': similar.abstract[:200] + '...' if similar.abstract else '',
            'year': similar.year.year if similar.year else None
        } for similar in similar_papers.items]
        # Basic paper info
        paper_data = {
            'paperId': paper.id,
            'title': paper.title,
            'abstract': paper.abstract,
            'year': paper.year.year if paper.year else None,
            'citations': formatted_citations,
            'similarPapers': formatted_similar_papers,
            'category': paper.category if paper.category else "",
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


@search_papers.route('/api/sameCategoryPapers/<string:id>', methods=['GET'])
def get_same_category(id):
    try:
        paper = Paper.query.get_or_404(id)
        # Fetch citations and similar papers (assuming relationships are defined in the Paper model)
        base_query = Paper.query.filter(
            Paper.category == paper.category
        )
        categories = base_query.paginate().items
        formatted_category_papers = [{
            'paperId': category.id,
            'title': category.title,
            'abstract': category.abstract,
            'year': category.year.year if category.year else None,
            'category': category.category if category.category else "",
        } for category in categories]
        print(categories)
        return jsonify({
            'status': 'success',
            'data':formatted_category_papers
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

##
# import numpy as np
# import pandas as pd
# import faiss
# csv_file_path = 'path/to/your/vectors.csv'
# data = pd.read_csv(csv_file_path)
#
# vectors = data.values.astype('float32')
# d = vectors.shape[1]
#
# index = faiss.IndexFlatL2(d)  # 使用L2距离
# index.add(vectors)  # 添加向量到索引
#
# query_vector = np.random.random((1, d)).astype('float32')  # 创建一个随机查询向量
# k = 4  # 近邻数量
# D, I = index.search(query_vector, k)
##
