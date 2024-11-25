from flask import Flask
from .config import Config
from .models import db, Paper  # 确保导入 Paper 模型
import csv
from datetime import datetime

def import_papers_from_csv(app, batch_size=1000):
    with app.app_context():
        db.create_all()
        try:
            # Read all existing titles first to reduce database queries
            existing_titles = set(p.title for p in Paper.query.with_entities(Paper.title).all())
            
            papers_to_add = []
            total_imported = 0
            
            with open('papers.csv', 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for row in csv_reader:
                    if row['title'] not in existing_titles:
                        paper = Paper(
                            title=row['title'],
                            abstract=row['abstract'],
                            category=row['category'],
                            year=datetime.strptime(row['year'], '%Y').date()
                        )
                        papers_to_add.append(paper)
                        
                        # Batch commit when reaching batch_size
                        if len(papers_to_add) >= batch_size:
                            db.session.bulk_save_objects(papers_to_add)
                            db.session.commit()
                            total_imported += len(papers_to_add)
                            papers_to_add = []
                            print(f"Imported {total_imported} papers...")
                
                # Commit remaining papers
                if papers_to_add:
                    db.session.bulk_save_objects(papers_to_add)
                    db.session.commit()
                    total_imported += len(papers_to_add)
                
                print(f"数据导入成功Total imported: {total_imported} papers")
                
        except Exception as e:
            print(f"导入数据时出错：{str(e)}")
            db.session.rollback()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化数据库
    db.init_app(app)
    
    # 导入数据
    import_papers_from_csv(app)

    return app
