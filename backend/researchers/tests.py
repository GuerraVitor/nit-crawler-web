from django.test import TestCase

from .lattes_runner import (
    FARMANGUINHOS_MEMBERS,
    InvalidLattesIdError,
    merge_members,
    normalize_lattes_id,
    parse_extra_ids,
)


class NormalizeLattesIdTests(TestCase):
    def test_accepts_16_digit_id(self):
        self.assertEqual(normalize_lattes_id("1234567890123456"), "1234567890123456")

    def test_strips_non_digit_characters(self):
        self.assertEqual(normalize_lattes_id(" 1234-5678 9012 3456 "), "1234567890123456")

    def test_rejects_short_id(self):
        with self.assertRaises(InvalidLattesIdError):
            normalize_lattes_id("12345")

    def test_rejects_empty_id(self):
        with self.assertRaises(InvalidLattesIdError):
            normalize_lattes_id("")

    def test_rejects_non_numeric_id(self):
        with self.assertRaises(InvalidLattesIdError):
            normalize_lattes_id("abcd567890123456")


class ParseExtraIdsTests(TestCase):
    def test_parses_valid_list(self):
        result = parse_extra_ids(["1234567890123456", "6543210987654321"])
        self.assertEqual(result, ["1234567890123456", "6543210987654321"])

    def test_ignores_blank_entries(self):
        result = parse_extra_ids(["1234567890123456", "", "   "])
        self.assertEqual(result, ["1234567890123456"])

    def test_dedupes_repeated_ids(self):
        result = parse_extra_ids(["1234567890123456", "1234567890123456"])
        self.assertEqual(result, ["1234567890123456"])

    def test_raises_on_first_invalid_id(self):
        with self.assertRaises(InvalidLattesIdError):
            parse_extra_ids(["1234567890123456", "not-an-id"])


class MergeMembersTests(TestCase):
    def test_appends_new_extra_ids_after_fixed_members(self):
        members, ignored = merge_members(["1111111111111111"])
        self.assertEqual(members[: len(FARMANGUINHOS_MEMBERS)], FARMANGUINHOS_MEMBERS)
        self.assertEqual(members[-1][0], "1111111111111111")
        self.assertEqual(ignored, [])

    def test_ignores_extra_id_that_duplicates_fixed_member(self):
        existing_id = FARMANGUINHOS_MEMBERS[0][0]
        members, ignored = merge_members([existing_id])
        self.assertEqual(members, FARMANGUINHOS_MEMBERS)
        self.assertEqual(ignored, [existing_id])

    def test_ignores_repeated_extra_ids(self):
        members, ignored = merge_members(["1111111111111111", "1111111111111111"])
        self.assertEqual(len(members), len(FARMANGUINHOS_MEMBERS) + 1)
        self.assertEqual(ignored, ["1111111111111111"])

    def test_no_extra_ids_returns_only_fixed_members(self):
        members, ignored = merge_members([])
        self.assertEqual(members, FARMANGUINHOS_MEMBERS)
        self.assertEqual(ignored, [])
