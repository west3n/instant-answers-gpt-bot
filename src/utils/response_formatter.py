import re


class TelegramMarkdownConverter:
    def __init__(self, text: str):
        self.text = text
        self.code_blocks = {}

    def combine_blockquotes(self) -> None:
        """
        Combines multiline blockquotes into a single blockquote while keeping the \n characters.
        """
        lines = self.text.split("\n")
        combined_lines = []
        blockquote_lines = []
        in_blockquote = False

        for line in lines:
            if line.startswith(">"):
                in_blockquote = True
                blockquote_lines.append(line[1:].strip())
            else:
                if in_blockquote:
                    combined_lines.append(
                        "<blockquote>" + "\n".join(blockquote_lines) + "</blockquote>"
                    )
                    blockquote_lines = []
                    in_blockquote = False
                combined_lines.append(line)

        if in_blockquote:
            combined_lines.append(
                "<blockquote>" + "\n".join(blockquote_lines) + "</blockquote>"
            )

        self.text = "\n".join(combined_lines)

    def convert_html_chars(self) -> None:
        """
        Converts HTML reserved symbols to their respective character references.
        """
        self.text = (
            self.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

    def split_by_tag(self, md_tag: str, html_tag: str) -> None:
        """
        Splits the text by Markdown tag and replaces it with the specified HTML tag.
        """
        tag_pattern = re.compile(
            r"(?<!\w){}(.*?){}(?!\w)".format(re.escape(md_tag), re.escape(md_tag)),
            re.DOTALL,
        )
        self.text = tag_pattern.sub(
            r"<{}>\1</{}>".format(html_tag, html_tag), self.text
        )

    def ensure_closing_delimiters(self) -> None:
        """
        Ensures that if an opening ` or ``` is found without a matching closing delimiter,
        the missing delimiter is appended to the end of the text.
        """
        if self.text.count("```") % 2 != 0:
            self.text += "```"
        if self.text.count("`") % 2 != 0:
            self.text += "`"

    def extract_and_convert_code_blocks(self) -> None:
        """
        Extracts code blocks from the text, converting them to HTML <pre><code> format,
        and replaces them with placeholders. Also ensures closing delimiters for unmatched blocks.
        """
        self.ensure_closing_delimiters()
        placeholders = []
        modified_text = self.text
        for match in re.finditer(r"```(\w*)?(\n)?(.*?)```", self.text, flags=re.DOTALL):
            language = match.group(1) if match.group(1) else ""
            code_content = match.group(3)
            placeholder = f"CODEBLOCKPLACEHOLDER{len(placeholders)}"
            placeholders.append(placeholder)
            if not language:
                html_code_block = f"<pre><code>{code_content}</code></pre>"
            else:
                html_code_block = f'<pre><code class="language-{language}">{code_content}</code></pre>'
            self.code_blocks[placeholder] = html_code_block
            modified_text = modified_text.replace(match.group(0), placeholder, 1)

        self.text = modified_text

    def reinsert_code_blocks(self) -> None:
        """
        Reinserts HTML code blocks into the text, replacing their placeholders.
        """
        for placeholder, html_code_block in self.code_blocks.items():
            self.text = self.text.replace(placeholder, html_code_block, 1)

    def remove_blockquote_escaping(self) -> None:
        """
        Removes the escaping from blockquote tags.
        """
        self.text = self.text.replace("&lt;blockquote&gt;", "<blockquote>").replace(
            "&lt;/blockquote&gt;", "</blockquote>"
        )

    def convert(self) -> str:
        """
        Converts markdown in the provided text to HTML supported by Telegram.
        """
        # Step 0: Combine blockquotes
        self.combine_blockquotes()

        # Step 1: Convert HTML reserved symbols
        self.convert_html_chars()

        # Step 2: Extract and convert code blocks first
        self.extract_and_convert_code_blocks()

        # Step 3: Escape HTML special characters in the output text
        self.text = self.text.replace("<", "&lt;").replace(">", "&gt;")

        # Inline code
        self.text = re.sub(r"`(.*?)`", r"<code>\1</code>", self.text)

        # Nested Bold and Italic
        self.text = re.sub(r"\*\*\*(.*?)\*\*\*", r"<b><i>\1</i></b>", self.text)
        self.text = re.sub(r"\_\_\_(.*?)\_\_\_", r"<u><i>\1</i></u>", self.text)

        # Process Markdown formatting tags (bold, underline, italic, strikethrough)
        # and convert them to their respective HTML tags
        self.split_by_tag("**", "b")
        self.split_by_tag("__", "u")
        self.split_by_tag("_", "i")
        self.split_by_tag("*", "i")
        self.split_by_tag("~~", "s")

        # Remove storage links
        self.text = re.sub(r"【[^】]+】", "", self.text)

        # Convert links
        self.text = re.sub(r"!?\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', self.text)

        # Convert headings
        self.text = re.sub(r"^\s*#+ (.+)", r"<b>\1</b>", self.text, flags=re.MULTILINE)

        # Convert unordered lists, preserving indentation
        self.text = re.sub(
            r"^(\s*)[\-\*] (.+)", r"\1• \2", self.text, flags=re.MULTILINE
        )

        # Step 4: Reinsert the converted HTML code blocks
        self.reinsert_code_blocks()

        # Step 5: Remove blockquote escaping
        self.remove_blockquote_escaping()

        return self.text
