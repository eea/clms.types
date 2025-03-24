# -*- coding: utf-8 -*-
"""Vocabulary for Product Family Titles"""

from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from clms.types.utils import get_taxonomy_tree


@implementer(IVocabularyFactory)
class DataSetAllFamilyTitles:
    """
    Vocabulary factory for product family titles.

    """

    def __call__(self, context):
        """
        Generates a vocabulary of all product family titles
        from taxonomy.
        """

        def find_matching_taxonomy(tree, parent_id):
            for node in tree:
                if node["key"] == parent_id:
                    # Return the children of the matching node
                    return node.get("children", [])
                # Recurse into children to find a match
                children = node.get("children", [])
                if children:
                    result = find_matching_taxonomy(children, parent_id)
                    if result:
                        return result

            return []  # Return an empty list if no match is found

        def traverse_taxonomy(tree, parent_title=""):
            """
            Recursively traverse taxonomy and collect terms.
            """
            terms = []
            for node in tree:
                key = str(node["key"])
                title = str(node["title"])
                # pylint: disable=line-too-long
                full_title = f"{parent_title} > {title}" if parent_title else title  # noqa
                # pylint: disable=line-too-long
                terms.append(SimpleTerm(value=key, token=key, title=full_title))  # noqa

                # Process children recursively
                children = node.get("children", [])
                if isinstance(children, list) and children:
                    terms.extend(traverse_taxonomy(children, full_title))
            return terms

        def find_all_products_taxonomy(tree):
            """
            Collect all products' children from the taxonomy tree.
            """
            all_products = []
            for node in tree:
                children = node.get("children", [])
                if children:
                    all_products.extend(children)
            return all_products

        # Retrieve the taxonomy tree
        try:
            taxonomy_tree = get_taxonomy_tree("collective.taxonomy.family")
        except Exception:
            taxonomy_tree = None

        if taxonomy_tree is None:
            return SimpleVocabulary([])

        all_products = find_all_products_taxonomy(taxonomy_tree)

        # Flatten the taxonomy into a list of SimpleTerms
        terms = traverse_taxonomy(all_products)

        sorted_terms = sorted(terms, key=lambda x: x.title.lower())

        # Return a SimpleVocabulary sorted by title
        return SimpleVocabulary(sorted_terms)


DataSetAllFamilyTitlesFactory = DataSetAllFamilyTitles()
