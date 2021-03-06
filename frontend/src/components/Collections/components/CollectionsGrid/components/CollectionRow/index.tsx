import { Intent, Tag } from "@blueprintjs/core";
import loadable from "@loadable/component";
import React, { FC } from "react";
import {
  ACCESS_TYPE,
  COLLECTION_LINK_TYPE,
  VISIBILITY_TYPE,
} from "src/common/entities";
import { useCollection } from "src/common/queries/collections";
import { StyledCell } from "../common/style";
import { LeftAlignedDetailsCell } from "./components/common/style";
import { aggregateDatasetsMetadata } from "./components/common/utils";
import {
  CollectionTitleText,
  RightAlignedDetailsCell,
  StyledRow,
} from "./style";

interface Props {
  id: string;
  accessType: ACCESS_TYPE;
  visibility: VISIBILITY_TYPE;
}

const AsyncPopover = loadable(
  () =>
    /*webpackChunkName: 'CollectionRow/components/Popover' */ import(
      "src/components/Collections/components/CollectionsGrid/components/CollectionRow/components/Popover"
    )
);

const conditionalPopover = (values: string[]) => {
  if (!values || values.length === 0) {
    return <LeftAlignedDetailsCell>-</LeftAlignedDetailsCell>;
  }

  return <AsyncPopover values={values} />;
};

type DOI = {
  doi: string;
  link: string;
};

const CollectionRow: FC<Props> = (props) => {
  const { data: collection } = useCollection(props.id, props.visibility);

  if (!collection) return null;

  // If there is an explicity accessType only show collections with that accessType
  if (props.accessType && collection.access_type !== props.accessType) {
    return null;
  }

  const { id, links, visibility, contact_name, name, datasets } = collection;

  const dois: Array<DOI> = links.reduce((acc, link) => {
    if (link.link_type !== COLLECTION_LINK_TYPE.DOI) return acc;

    const url = new URL(link.link_url);

    acc.push({ doi: url.pathname.substring(1), link: link.link_url });

    return acc;
  }, [] as DOI[]);

  const isPrivate = visibility === VISIBILITY_TYPE.PRIVATE;

  const {
    tissue,
    assay,
    disease,
    organism,
    cell_count,
  } = aggregateDatasetsMetadata(datasets);

  return (
    <StyledRow>
      <StyledCell>
        <CollectionTitleText
          href={`/collections/${id}${isPrivate ? "/private" : ""}`}
        >
          {name}
        </CollectionTitleText>
        <div>{contact_name}</div>

        {props.accessType === ACCESS_TYPE.WRITE ? (
          <Tag minimal intent={isPrivate ? Intent.PRIMARY : Intent.SUCCESS}>
            {isPrivate ? "Private" : "Published"}
          </Tag>
        ) : (
          dois?.map((doi) => (
            <a key={doi.doi} href={doi.link}>
              {doi.doi}
            </a>
          ))
        )}
      </StyledCell>
      {conditionalPopover(tissue)}
      {conditionalPopover(assay)}
      {conditionalPopover(disease)}
      {conditionalPopover(organism)}
      <RightAlignedDetailsCell>{cell_count || "-"}</RightAlignedDetailsCell>
    </StyledRow>
  );
};

export default CollectionRow;
