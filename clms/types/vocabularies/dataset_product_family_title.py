# -*- coding: utf-8 -*-
"""Dynamic vocabulary for Product Family Titles"""
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from clms.types.utils import get_taxonomy_tree


@implementer(IVocabularyFactory)
class DataSetProductFamilyTitle:
    """
    Vocabulary factory for product family titles.

    Logic for determining the vocabulary:
    - If the request comes from a dataset URL:
        /product/dataset => parent_id = product
    - Else:
        parent_id = None

    If the product name exists and is found in the taxonomy:
        vocabulary = taxonomy(product)
    If the product name exists but is not found in the taxonomy:
        vocabulary = []
    If the product name doesn't exist (None):
        vocabulary = taxonomy(all_products)
    """

    def __call__(self, context):
        """
        Generates a vocabulary of product family titles
        from taxonomy, filtered by parent title.
        """

        parent_id = None
        try:
            # Get the parent title of the current dataset
            parent_title = context.REQUEST.get("HTTP_REFERER")
            parts = [p for p in parent_title.split("/") if p and not p.startswith("edit")]  # noqa
            parent_id = parts[-2] if "products" in parts else None
        except Exception:
            parent_title = None

        def find_matching_taxonomy(tree, parent_id):
            """
            Find the taxonomy node(s) with a title matching the parent title.
            """
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

        # Determine the filtered tree based on parent_id
        if parent_id is None:
            # No parent_id, return all products
            filtered_tree = find_all_products_taxonomy(taxonomy_tree)
        else:
            # Filter by parent_id
            filtered_tree = find_matching_taxonomy(taxonomy_tree, parent_id)

        # Flatten the filtered taxonomy into a list of SimpleTerms
        terms = traverse_taxonomy(filtered_tree)

        sorted_terms = sorted(terms, key=lambda x: x.title.lower())

        # Return a SimpleVocabulary sorted by title
        return SimpleVocabulary(sorted_terms)


DataSetProductFamilyTitleFactory = DataSetProductFamilyTitle()
