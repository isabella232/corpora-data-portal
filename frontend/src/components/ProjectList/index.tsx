import React, { FC } from "react";
import { Project as IProject } from "src/common/entities";
import Dataset from "./components/Dataset";
import Heading from "./components/Heading";

interface Props {
  projects: IProject[];
}

const ProjectsList: FC<Props> = ({ projects }) => {
  if (!projects) return <div>Sorry, we could not find any projects</div>;

  return (
    <>
      <Heading />
      {projects
        .flatMap(project =>
          project.datasets.map(dataset => ({ dataset, links: project.links }))
        )
        .map(({ dataset, links }) => (
          <Dataset key={dataset.id} dataset={dataset} links={links} />
        ))}
    </>
  );
};

export default ProjectsList;