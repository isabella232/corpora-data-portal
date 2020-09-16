import React, { FC } from "react";
import { Project } from "src/common/entities";
import { SmallColumn } from "../../common/style";
import { StyledAnchor, Wrapper } from "./style";
interface AnchorProps {
  url: string;
}

const Anchor: FC<AnchorProps> = ({ url, children }) => {
  return (
    <StyledAnchor href={url} target="_blank" rel="noopener">
      {children}
    </StyledAnchor>
  );
};

interface Props {
  links: Project["links"];
}

const MoreInformation: FC<Props> = ({ links }) => {
  const uniqueLinks = Array.from(
    new Map(links.map((link) => [link.url, link.name]))
  );

  const styledLinks = uniqueLinks.map((link) => {
    const [url, name] = link;

    return (
      <div key={url}>
        <Anchor url={url}>{name}</Anchor>
      </div>
    );
  });

  return (
    <SmallColumn>
      <Wrapper>{styledLinks}</Wrapper>
    </SmallColumn>
  );
};

export default MoreInformation;
